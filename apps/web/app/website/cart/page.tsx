"use client";

import React, { useState } from "react";
import Link from "next/link";

interface CartItem {
  id: string;
  name: string;
  price: number;
  qty: number;
  chiefDrug: string;
  lotAllocated: string;
}

export default function CartPage() {
  const [items, setItems] = useState<CartItem[]>([
    {
      id: "manivital-pro",
      name: "ManiVital Pro",
      price: 1450,
      qty: 1,
      chiefDrug: "Withania somnifera & Mucuna pruriens",
      lotAllocated: "BMR-2026-MVP-09 (FEFO: Exp 2028-09)",
    },
    {
      id: "metabocore-elite",
      name: "MetaboCore Elite",
      price: 1250,
      qty: 1,
      chiefDrug: "Gymnema sylvestre & Momordica charantia",
      lotAllocated: "BMR-2026-MET-03 (FEFO: Exp 2028-06)",
    },
  ]);

  const [couponCode, setCouponCode] = useState("");
  const [discountPct, setDiscountPct] = useState(0);
  const [couponMessage, setCouponMessage] = useState<string | null>(null);

  // Customer Checkout Form
  const [fullName, setFullName] = useState("Mohammad Tariq");
  const [email, setEmail] = useState("tariq.m@example.com");
  const [phone, setPhone] = useState("+91 98765 43210");
  const [address, setAddress] = useState("Flat 402, Hamdard Enclave, Jamia Nagar");
  const [city, setCity] = useState("New Delhi");
  const [pincode, setPincode] = useState("110025");
  const [paymentMethod, setPaymentMethod] = useState<"upi" | "card" | "cod">("upi");
  const [isOrdered, setIsOrdered] = useState(false);
  const [orderReceipt, setOrderReceipt] = useState<any>(null);

  const rawSubtotal = items.reduce((sum, item) => sum + item.price * item.qty, 0);
  const discountAmount = Math.round((rawSubtotal * discountPct) / 100);
  const shippingFee = rawSubtotal > 1500 ? 0 : 99;
  const grandTotal = rawSubtotal - discountAmount + shippingFee;

  const updateQty = (id: string, delta: number) => {
    setItems((prev) =>
      prev
        .map((item) => {
          if (item.id === id) {
            const newQty = item.qty + delta;
            return newQty > 0 ? { ...item, qty: newQty } : null;
          }
          return item;
        })
        .filter(Boolean) as CartItem[]
    );
  };

  const removeItem = (id: string) => {
    setItems(items.filter((i) => i.id !== id));
  };

  const applyCoupon = (e: React.FormEvent) => {
    e.preventDefault();
    if (couponCode.toUpperCase() === "UNANI10") {
      setDiscountPct(10);
      setCouponMessage("✓ Coupon UNANI10 applied! 10% discount deducted.");
    } else if (couponCode.toUpperCase() === "UNANI15" || couponCode.toUpperCase() === "ZAYVORA15") {
      setDiscountPct(15);
      setCouponMessage("✓ Coupon UNANI15 applied! 15% discount deducted.");
    } else {
      setCouponMessage("✕ Invalid coupon code. Try UNANI10 or UNANI15.");
    }
  };

  const handleCheckout = (e: React.FormEvent) => {
    e.preventDefault();
    const orderId = `ORD-ZY-${Math.floor(100000 + Math.random() * 900000)}`;
    const receipt = {
      orderId,
      customer: fullName,
      phone,
      address: `${address}, ${city} - ${pincode}`,
      itemsCount: items.length,
      grandTotal,
      paymentMethod: paymentMethod.toUpperCase(),
      fefoBatches: items.map((i) => `${i.name}: ${i.lotAllocated}`),
      timestamp: new Date().toISOString(),
    };
    setOrderReceipt(receipt);
    setIsOrdered(true);
  };

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Herbals Dispensary</span>
          <h1 className="text-3xl font-extrabold text-white mt-1">Prescription & Botanical Cart</h1>
          <p className="text-sm text-[#94A3B8]">Direct Dispensary Fulfillment with Automated FEFO Batch Allocation.</p>
        </div>
        <Link href="/website/herbals" className="text-xs font-semibold text-[#2DD4BF] hover:underline">
          ← Back to Herbals Catalog
        </Link>
      </div>

      {isOrdered ? (
        <div className="p-8 rounded-3xl bg-[#0F172A] border border-emerald-500/40 text-center space-y-6 shadow-2xl">
          <div className="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 text-3xl font-bold flex items-center justify-center mx-auto border border-emerald-500/50">
            ✓
          </div>
          <div>
            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Payment & Order Verified</span>
            <h2 className="text-2xl font-extrabold text-white mt-1">Order Placed Successfully!</h2>
            <p className="text-sm text-slate-300 mt-2">
              Order ID: <span className="font-mono font-bold text-emerald-300">{orderReceipt?.orderId}</span>
            </p>
          </div>

          <div className="max-w-lg mx-auto bg-[#1E293B] p-6 rounded-2xl border border-[#334155] text-left space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider border-b border-[#334155] pb-2">
              Dispensary FEFO Allocation Receipt
            </h4>
            <div className="flex justify-between">
              <span className="text-[#94A3B8]">Recipient:</span>
              <span className="text-white font-semibold">{orderReceipt?.customer}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#94A3B8]">Delivery Destination:</span>
              <span className="text-white text-right font-medium max-w-xs">{orderReceipt?.address}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#94A3B8]">Payment Channel:</span>
              <span className="text-emerald-400 font-bold">{orderReceipt?.paymentMethod} (Verified Instant)</span>
            </div>
            <div className="flex justify-between border-t border-[#334155] pt-2">
              <span className="text-[#94A3B8]">Total Settled:</span>
              <span className="text-lg font-bold text-white">₹{orderReceipt?.grandTotal?.toLocaleString("en-IN")}</span>
            </div>

            <div className="pt-2">
              <span className="text-[10px] text-[#2DD4BF] font-bold block uppercase">Allocated Batch Lots:</span>
              {orderReceipt?.fefoBatches?.map((b: string, idx: number) => (
                <div key={idx} className="text-[11px] font-mono text-slate-300">• {b}</div>
              ))}
            </div>
          </div>

          <div className="pt-4 flex justify-center gap-4">
            <Link href="/website/herbals" className="px-6 py-3 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-xs">
              Continue Shopping
            </Link>
            <Link href="/patient" className="px-6 py-3 rounded-xl bg-[#1E293B] border border-[#334155] hover:text-white text-[#CBD5E1] font-semibold text-xs">
              View in Patient Portal
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Cart Item List */}
          <div className="lg:col-span-7 space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Shopping Basket ({items.length} Formulations)</h3>
            
            {items.map((item) => (
              <div key={item.id} className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                <div className="space-y-1">
                  <h4 className="font-bold text-white text-base">{item.name}</h4>
                  <p className="text-xs text-[#94A3B8]">{item.chiefDrug}</p>
                  <span className="text-[10px] font-mono text-[#2DD4BF] block bg-[#0F172A] px-2 py-0.5 rounded w-fit">
                    {item.lotAllocated}
                  </span>
                </div>

                <div className="flex items-center justify-between sm:justify-end gap-5">
                  <div className="flex items-center gap-2 bg-[#0F172A] border border-[#334155] rounded-xl px-2 py-1">
                    <button onClick={() => updateQty(item.id, -1)} className="px-2 py-0.5 text-base font-bold text-[#94A3B8] hover:text-white">-</button>
                    <span className="font-bold text-white px-2">{item.qty}</span>
                    <button onClick={() => updateQty(item.id, 1)} className="px-2 py-0.5 text-base font-bold text-[#94A3B8] hover:text-white">+</button>
                  </div>

                  <span className="font-extrabold text-white text-sm">₹{(item.price * item.qty).toLocaleString("en-IN")}</span>

                  <button onClick={() => removeItem(item.id)} className="text-rose-400 hover:text-rose-300 text-base font-bold">✕</button>
                </div>
              </div>
            ))}

            {items.length === 0 && (
              <div className="p-8 rounded-2xl bg-[#1E293B] border border-[#334155] text-center space-y-3">
                <p className="text-sm text-[#94A3B8]">Your dispensary basket is currently empty.</p>
                <Link href="/website/herbals" className="inline-block px-5 py-2 rounded-xl bg-[#0D9488] text-white font-bold text-xs">
                  Browse 10 Standardized Formulations
                </Link>
              </div>
            )}

            {/* Promo Code Input */}
            <form onSubmit={applyCoupon} className="p-4 rounded-xl bg-[#1E293B] border border-[#334155] flex items-center gap-3">
              <input
                type="text"
                value={couponCode}
                onChange={(e) => setCouponCode(e.target.value)}
                placeholder="Promo / Clinical Coupon (e.g. UNANI10)"
                className="flex-1 bg-[#0F172A] border border-[#334155] rounded-xl px-3 py-2 text-white uppercase text-xs"
              />
              <button type="submit" className="px-4 py-2 bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold rounded-xl text-xs">
                Apply Code
              </button>
            </form>
            {couponMessage && <p className="text-xs text-[#2DD4BF] font-semibold">{couponMessage}</p>}
          </div>

          {/* Checkout & Delivery Summary */}
          <div className="lg:col-span-5 space-y-4">
            <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-4">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">Delivery & Patient Information</h3>

              <form onSubmit={handleCheckout} className="space-y-3">
                <div>
                  <label className="text-[10px] text-[#94A3B8] font-bold block mb-1">PATIENT / RECIPIENT NAME</label>
                  <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    required
                    className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-3 py-2 text-white text-xs"
                  />
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-[10px] text-[#94A3B8] font-bold block mb-1">PHONE NUMBER</label>
                    <input
                      type="tel"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      required
                      className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-3 py-2 text-white text-xs"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] text-[#94A3B8] font-bold block mb-1">EMAIL ADDRESS</label>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-3 py-2 text-white text-xs"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-[10px] text-[#94A3B8] font-bold block mb-1">DELIVERY ADDRESS</label>
                  <input
                    type="text"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    required
                    className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-3 py-2 text-white text-xs"
                  />
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-[10px] text-[#94A3B8] font-bold block mb-1">CITY</label>
                    <input
                      type="text"
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      required
                      className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-3 py-2 text-white text-xs"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] text-[#94A3B8] font-bold block mb-1">PINCODE</label>
                    <input
                      type="text"
                      value={pincode}
                      onChange={(e) => setPincode(e.target.value)}
                      required
                      className="w-full bg-[#0F172A] border border-[#334155] rounded-xl px-3 py-2 text-white text-xs"
                    />
                  </div>
                </div>

                {/* Payment Options */}
                <div className="pt-2">
                  <label className="text-[10px] text-[#94A3B8] font-bold block mb-1.5">PAYMENT METHOD</label>
                  <div className="grid grid-cols-3 gap-2">
                    <button
                      type="button"
                      onClick={() => setPaymentMethod("upi")}
                      className={`py-2 rounded-xl text-xs font-bold border transition ${
                        paymentMethod === "upi" ? "bg-[#0D9488] border-[#2DD4BF] text-white" : "bg-[#0F172A] border-[#334155] text-[#94A3B8]"
                      }`}
                    >
                      ⚡ UPI
                    </button>
                    <button
                      type="button"
                      onClick={() => setPaymentMethod("card")}
                      className={`py-2 rounded-xl text-xs font-bold border transition ${
                        paymentMethod === "card" ? "bg-[#0D9488] border-[#2DD4BF] text-white" : "bg-[#0F172A] border-[#334155] text-[#94A3B8]"
                      }`}
                    >
                      💳 Card
                    </button>
                    <button
                      type="button"
                      onClick={() => setPaymentMethod("cod")}
                      className={`py-2 rounded-xl text-xs font-bold border transition ${
                        paymentMethod === "cod" ? "bg-[#0D9488] border-[#2DD4BF] text-white" : "bg-[#0F172A] border-[#334155] text-[#94A3B8]"
                      }`}
                    >
                      📦 COD
                    </button>
                  </div>
                </div>

                {/* Pricing Summary */}
                <div className="border-t border-[#334155] pt-3 space-y-1.5 text-[11px]">
                  <div className="flex justify-between text-[#94A3B8]">
                    <span>Formulations Subtotal:</span>
                    <span>₹{rawSubtotal.toLocaleString("en-IN")}</span>
                  </div>
                  {discountAmount > 0 && (
                    <div className="flex justify-between text-emerald-400">
                      <span>Clinical Discount ({discountPct}%):</span>
                      <span>-₹{discountAmount.toLocaleString("en-IN")}</span>
                    </div>
                  )}
                  <div className="flex justify-between text-[#94A3B8]">
                    <span>Dispensary Cold-Chain Courier:</span>
                    <span>{shippingFee === 0 ? "FREE (Orders > ₹1500)" : `₹${shippingFee}`}</span>
                  </div>
                  <div className="flex justify-between text-white font-extrabold text-sm border-t border-[#334155] pt-2">
                    <span>Grand Total:</span>
                    <span className="text-[#2DD4BF]">₹{grandTotal.toLocaleString("en-IN")}</span>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={items.length === 0}
                  className="w-full py-3.5 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] disabled:opacity-50 text-white font-extrabold text-xs shadow-lg transition mt-2"
                >
                  Place Dispensary Order (₹{grandTotal.toLocaleString("en-IN")}) →
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
