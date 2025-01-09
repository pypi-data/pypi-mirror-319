package main

import (
    "encoding/json"
    "fmt"
    "time"

    "github.com/hyperledger/fabric-contract-api-go/contractapi"
    // "github.com/hyperledger/fabric-contract-api-go/metadata"
)

// EscrowContract implements the Hyperledger Fabric smart contract logic.
type EscrowContract struct {
    contractapi.Contract
}

// Escrow describes the main attributes of the escrow on the public ledger
type Escrow struct {
    EscrowID     string        `json:"escrowId"`
    ProductID    string        `json:"productId"`
    BuyerID      string        `json:"buyerId"`
    SellerID     string        `json:"sellerId"`
    TotalAmount  float64       `json:"totalAmount"`
    BalancePaid  float64       `json:"balancePaid"`
    Status       string        `json:"status"` // CREATED, ACTIVE, DELIVERED, RELEASED, REFUNDED
    IsLayaway    bool          `json:"isLayaway"`
    Installments []Installment `json:"installments"`
    CreatedAt    string        `json:"createdAt"`
    DeliveryTime string        `json:"deliveryTime"`
    ReleasedAt   string        `json:"releasedAt"`
    RefundedAt   string        `json:"refundedAt"`
}

// Installment is used if we have a layaway plan
type Installment struct {
    Amount float64 `json:"amount"`
    PaidAt string  `json:"paidAt"`
}

// PrivateData captures sensitive info stored in the private data collection
type PrivateData struct {
    // If you want to keep it purely among only two orgs
    // but the entire channel PDC might include more orgs,
    // you can store data in encrypted form:
    EncryptedPayload string `json:"encryptedPayload"`
}

// CreateEscrow creates a new escrow record on the ledger and puts some sensitive data in the PDC.
func (c *EscrowContract) CreateEscrow(ctx contractapi.TransactionContextInterface, escrowId, productId, buyerId, sellerId string, totalAmount float64, isLayaway bool, encryptedPayload string) error {
    // Check if escrow already exists
    existing, err := ctx.GetStub().GetState(escrowId)
    if err != nil {
        return fmt.Errorf("failed to check escrow existence: %v", err)
    }
    if len(existing) > 0 {
        return fmt.Errorf("escrow %s already exists", escrowId)
    }

    newEscrow := Escrow{
        EscrowID:     escrowId,
        ProductID:    productId,
        BuyerID:      buyerId,
        SellerID:     sellerId,
        TotalAmount:  totalAmount,
        BalancePaid:  0,
        Status:       "CREATED",
        IsLayaway:    isLayaway,
        Installments: []Installment{},
        CreatedAt:    time.Now().UTC().Format(time.RFC3339),
    }

    escrowBytes, err := json.Marshal(newEscrow)
    if err != nil {
        return fmt.Errorf("failed to marshal new escrow: %v", err)
    }

    // Put escrow on public ledger
    err = ctx.GetStub().PutState(escrowId, escrowBytes)
    if err != nil {
        return fmt.Errorf("failed to put escrow on state: %v", err)
    }

    // optional: store private data in the PDC.
    privData := PrivateData{
        EncryptedPayload: encryptedPayload,
    }
    privBytes, _ := json.Marshal(privData)

    // The collection name must match what you declared in collections_config.json
    collectionName := "escrowPDC"

    err = ctx.GetStub().PutPrivateData(collectionName, escrowId, privBytes)
    if err != nil {
        return fmt.Errorf("failed to put private data: %v", err)
    }

    return nil
}

// PayInstallment is for partial payments in a layaway scenario (or to pay in full if not layaway).
func (c *EscrowContract) PayInstallment(ctx contractapi.TransactionContextInterface, escrowId string, amount float64) error {
    escrowBytes, err := ctx.GetStub().GetState(escrowId)
    if err != nil {
        return fmt.Errorf("error reading escrow: %v", err)
    }
    if len(escrowBytes) == 0 {
        return fmt.Errorf("escrow %s not found", escrowId)
    }

    var escrow Escrow
    err = json.Unmarshal(escrowBytes, &escrow)
    if err != nil {
        return fmt.Errorf("unmarshal error: %v", err)
    }

    if escrow.Status != "CREATED" && escrow.Status != "ACTIVE" {
        return fmt.Errorf("cannot pay installment in status: %s", escrow.Status)
    }

    // ────────────────────────────────────────────────────────────
    // NEW CHECK: forbid partial payments on non-layaway escrows.
    // We require paying the entire total in one go if not layaway.
    if !escrow.IsLayaway {
        // If escrow is not layaway and there's already some balancePaid, that means
        // there's already been a payment. We don't allow more than one partial payment.
        if escrow.BalancePaid > 0 {
            return fmt.Errorf("escrow is not layaway; partial payments are not allowed. This escrow already received a payment.")
        }

        // If user tries to pay something other than exactly totalAmount in a single shot
        // for a non-layaway, forbid it.
        if amount != escrow.TotalAmount {
            return fmt.Errorf("non-layaway escrows must be paid in full in a single transaction, expected %.2f, got %.2f", escrow.TotalAmount, amount)
        }
    }
    // ────────────────────────────────────────────────────────────

    escrow.BalancePaid += amount
    if escrow.Status == "CREATED" {
        escrow.Status = "ACTIVE"
    }
    if escrow.IsLayaway {
        newInst := Installment{
            Amount: amount,
            PaidAt: time.Now().UTC().Format(time.RFC3339),
        }
        escrow.Installments = append(escrow.Installments, newInst)
    }

    escrowUpdatedBytes, err := json.Marshal(escrow)
    if err != nil {
        return fmt.Errorf("failed to marshal updated escrow: %v", err)
    }

    err = ctx.GetStub().PutState(escrowId, escrowUpdatedBytes)
    if err != nil {
        return fmt.Errorf("failed to update escrow: %v", err)
    }

    return nil
}

// ConfirmDelivery sets the status to DELIVERED
func (c *EscrowContract) ConfirmDelivery(ctx contractapi.TransactionContextInterface, escrowId string) error {
    escrowBytes, err := ctx.GetStub().GetState(escrowId)
    if err != nil {
        return err
    }
    if len(escrowBytes) == 0 {
        return fmt.Errorf("escrow %s not found", escrowId)
    }

    var escrow Escrow
    err = json.Unmarshal(escrowBytes, &escrow)
    if err != nil {
        return err
    }

    if escrow.Status != "ACTIVE" {
        return fmt.Errorf("escrow not active")
    }
    escrow.Status = "DELIVERED"
    escrow.DeliveryTime = time.Now().UTC().Format(time.RFC3339)

    updated, err := json.Marshal(escrow)
    if err != nil {
        return fmt.Errorf("failed to marshal escrow for delivery update: %v", err)
    }

    return ctx.GetStub().PutState(escrowId, updated)
}

// ReleaseFunds moves to RELEASED if conditions are met
func (c *EscrowContract) ReleaseFunds(ctx contractapi.TransactionContextInterface, escrowId string) error {
    escrowBytes, err := ctx.GetStub().GetState(escrowId)
    if err != nil {
        return err
    }
    if len(escrowBytes) == 0 {
        return fmt.Errorf("escrow %s not found", escrowId)
    }

    var escrow Escrow
    err = json.Unmarshal(escrowBytes, &escrow)
    if err != nil {
        return err
    }

    if escrow.Status != "DELIVERED" {
        return fmt.Errorf("must be DELIVERED to release funds")
    }
    if escrow.BalancePaid < escrow.TotalAmount {
        return fmt.Errorf("insufficient payment: paid %f, needed %f", escrow.BalancePaid, escrow.TotalAmount)
    }
    escrow.Status = "RELEASED"
    escrow.ReleasedAt = time.Now().UTC().Format(time.RFC3339)

    updated, err := json.Marshal(escrow)
    if err != nil {
        return fmt.Errorf("failed to marshal escrow for release: %v", err)
    }

    return ctx.GetStub().PutState(escrowId, updated)
}

// ReimburseBuyer refunds if not delivered, etc.
func (c *EscrowContract) ReimburseBuyer(ctx contractapi.TransactionContextInterface, escrowId string) error {
    escrowBytes, err := ctx.GetStub().GetState(escrowId)
    if err != nil {
        return err
    }
    if len(escrowBytes) == 0 {
        return fmt.Errorf("escrow %s not found", escrowId)
    }

    var escrow Escrow
    err = json.Unmarshal(escrowBytes, &escrow)
    if err != nil {
        return err
    }

    if escrow.Status == "RELEASED" {
        return fmt.Errorf("cannot reimburse after funds released")
    }

    escrow.Status = "REFUNDED"
    escrow.RefundedAt = time.Now().UTC().Format(time.RFC3339)

    updated, err := json.Marshal(escrow)
    if err != nil {
        return fmt.Errorf("failed to marshal escrow for refund: %v", err)
    }

    return ctx.GetStub().PutState(escrowId, updated)
}

// ReadEscrow returns the public portion
func (c *EscrowContract) ReadEscrow(ctx contractapi.TransactionContextInterface, escrowId string) (*Escrow, error) {
    escrowBytes, err := ctx.GetStub().GetState(escrowId)
    if err != nil {
        return nil, err
    }
    if len(escrowBytes) == 0 {
        return nil, fmt.Errorf("not found")
    }
    var e Escrow
    err = json.Unmarshal(escrowBytes, &e)
    if err != nil {
        return nil, err
    }
    return &e, nil
}

// ReadPrivateData returns encrypted payload from PDC
func (c *EscrowContract) ReadPrivateData(ctx contractapi.TransactionContextInterface, escrowId string) (string, error) {
    collectionName := "escrowPDC"
    privDataBytes, err := ctx.GetStub().GetPrivateData(collectionName, escrowId)
    if err != nil {
        return "", fmt.Errorf("error reading private data: %v", err)
    }
    if len(privDataBytes) == 0 {
        return "", fmt.Errorf("no private data found for %s", escrowId)
    }

    var p PrivateData
    err = json.Unmarshal(privDataBytes, &p)
    if err != nil {
        return "", fmt.Errorf("failed to unmarshal private data: %v", err)
    }

    return p.EncryptedPayload, nil
}

func main() {
    chaincode, err := contractapi.NewChaincode(new(EscrowContract))
    if err != nil {
        panic(fmt.Sprintf("Error creating escrow chaincode: %v", err))
    }

    // By commenting these out, Fabric won't generate an OpenAPI schema
    // that marks omitted fields as required.
    // chaincode.Info.Title = "EscrowChaincode"
    // chaincode.Info.Version = "0.1"
    // chaincode.Info.Contact = &metadata.ContactInfo{
    //     Name:  "Your Name",
    //     Email: "example@example.com",
    // }

    if err := chaincode.Start(); err != nil {
        panic(fmt.Sprintf("Error starting escrow chaincode: %v", err))
    }
}