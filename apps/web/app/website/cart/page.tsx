"use client";

import React, { useState } from "react";
import Link from "next/link";

export default function CartPage() {
  const [items, setItems] = useState([
    { id: "manivital-pro", name: "ManiVital Pro", price: 1450, qty: 1 },
    { id: "metabocore-elite", name: "MetaboCore Elite", price: 1250, qty: 1 }
  ]);
  const [isOrdered, setIsOrdered] = useState(false);

  const subtotal = items.reduce((sum, item) => sum + item.price * item.qty, 0);

  function removeItem(id: string) {
    setItems(items.filter(i => i.id !== id));
  }

  function handleCheckout(e: React.FormEvent) {
    e.preventDefault();
    setIsOrdered(true);
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      <div className="border-b border-[#334155] pb-4">
        <h1 className="text-2xl font-bold text-white">Your ZAYVORA Herbals Cart</h1>
        <p className="text-[#94A3B8]">Direct Dispensary Order with FEFO Guaranteed Freshness</p>
      </div>

      {isOrdered ? (
        <div className="p-8 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-center space-y-3">
          <span className="text-4xl block">✓</span>
          <h2 className="text-xl font-bold text-white">Order Confirmed & Placed!</h2>
          <p className="text-sm text-emerald-300">
            Order <span className="font-mono font-bold text-white">ORD-ZY-8812</span> has been received by our Central Dispensary. Your botanicals are allocated from verified batch lots and will be dispatched within 24 hours.
          </p>
          <Link href="/website/herbals" className="inline-block mt-4 px-6 py-2.5 rounded-xl bg-[#0D9488] text-white font-bold text-xs">
            Continue Shopping
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2 space-y-4">
            {items.map((item) => (
              <div key={item.id} className="p-4 rounded-xl bg-[#1E293B] border border-[#334155] flex justify-between items-center">
                <div>
                  <h4 className="font-bold text-white text-sm">{item.name}</h4>
                  <span className="text-[#94A3B8]">Qty: {item.qty} × ₹{item.price}</span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="font-bold text-white">₹{item.price * item.qty}</span>
                  <button onClick={() => removeItem(item.id)} className="text-rose-400 hover:text-rose-300">✕</button>
                </div>
              </div>
            ))}
            {items.length === 0 && (
              <p className="text-[#94A3B8] text-center py-8">Your cart is empty. <Link href="/website/herbals" className="text-emerald-400 underline">Explore Formulations</Link></p>
            )}
          </div>

          <div className="p-5 rounded-2xl bg-[#0F172A] border border-[#334155] space-y-4 h-fit">
            <h3 className="font-bold text-white text-sm border-b border-[#334155] pb-2">Order Summary</h3>
            <div className="space-y-1.5">
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Subtotal:</span>
                <span className="text-white">₹{subtotal}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Courier Shipping:</span>
                <span className="text-emerald-400 font-semibold">FREE</span>
              </div>
              <div className="flex justify-between pt-2 border-t border-[#334155] font-bold">
                <span className="text-white">Total:</span>
                <span className="text-emerald-400 text-sm">₹{subtotal}</span>
              </div>
            </div>

            <form onSubmit={handleCheckout} className="space-y-3 pt-2">
              <input placeholder="Shipping Address..." className="w-full px-3 py-2 rounded-lg bg-[#1E293B] border border-[#334155] text-white" required />
              <input placeholder="Contact Phone..." defaultValue="+91-9876543210" className="w-full px-3 py-2 rounded-lg bg-[#1E293B] border border-[#334155] text-white" required />
              <button disabled={items.length === 0} type="submit" className="w-full py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-xs disabled:opacity-50">
                Proceed to Checkout
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
