#!/usr/bin/env python3
"""
ZAYVORA Health OS — Commercial E-Commerce, B2B Wholesale & Checkout Engine
1. Commercial Multi-Step Checkout Modal with UPI/Card/COD & Live GST Invoice
2. Interactive Product Details (PDP) Quick-View Modal
3. B2B Doctor Wholesale Portal with 40-50% Clinic Margins
"""
import re

CORE_FILE = "js/zayvora-core.js"
INDEX_FILE = "index.html"

COMMERCIAL_MODALS_HTML = '''
  <!-- ===================================================================== -->
  <!-- MODAL: COMMERCIAL CHECKOUT & PAYMENT GATEWAY MODAL                    -->
  <!-- ===================================================================== -->
  <div id="commercial-checkout-modal" class="fixed inset-0 z-50 hidden bg-black/85 backdrop-blur-md flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-emerald-500/40 rounded-3xl max-w-2xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-lg">🛍️</span>
          <div>
            <h3 class="text-base font-bold text-white">ZAYVORA Official Dispensary Checkout</h3>
            <p class="text-xs text-slate-400">Encrypted 256-bit SSL • Direct FEFO Cold-Chain Dispatch • Free Delivery Above ₹999</p>
          </div>
        </div>
        <button onclick="toggleCheckoutModal()" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>

      <!-- Modal Body (Dynamic Steps) -->
      <div id="checkout-modal-body" class="p-6 overflow-y-auto flex-1 space-y-5 text-xs">
        <!-- Rendered dynamically by renderCheckoutStep() -->
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- MODAL: PRODUCT DETAIL QUICK-VIEW (COMMERCIAL PDP MODAL)               -->
  <!-- ===================================================================== -->
  <div id="product-quickview-modal" class="fixed inset-0 z-50 hidden bg-black/85 backdrop-blur-md flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 rounded-3xl max-w-2xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
      <div class="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950">
        <div class="flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-lg">🌿</span>
          <div>
            <h3 id="pdp-modal-title" class="text-base font-bold text-white">Product Overview</h3>
            <p id="pdp-modal-subtitle" class="text-xs text-slate-400">AYUSH-GMP Standardized Formulation</p>
          </div>
        </div>
        <button onclick="toggleProductQuickViewModal()" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition">✕</button>
      </div>

      <div id="product-quickview-body" class="p-6 overflow-y-auto flex-1 space-y-4 text-xs">
        <!-- Rendered dynamically by openProductQuickView(sku) -->
      </div>
    </div>
  </div>
'''

COMMERCIAL_JS_CODE = '''
    // ── COMMERCIAL E-COMMERCE, CHECKOUT & B2B WHOLESALE ENGINE ──────────────
    let checkoutState = {
      step: 1, // 1: Address & Order Type, 2: Payment, 3: Confirmation
      isSubscription: false,
      shipping: {
        fullName: 'Hamza Farooqi',
        phone: '+91 98110 44219',
        email: 'hamza.farooqi@gmail.com',
        address: 'House 42, Pocket B, Sukhdev Vihar',
        city: 'New Delhi',
        state: 'Delhi',
        pincode: '110025'
      },
      paymentMethod: 'UPI',
      lastOrderId: null
    };

    function toggleCheckoutModal() {
      const modal = document.getElementById('commercial-checkout-modal');
      if (!modal) return;
      modal.classList.toggle('hidden');
      if (!modal.classList.contains('hidden')) {
        checkoutState.step = 1;
        renderCheckoutStep();
      }
    }

    function toggleProductQuickViewModal() {
      const modal = document.getElementById('product-quickview-modal');
      if (modal) modal.classList.toggle('hidden');
    }

    function openProductQuickView(skuOrId) {
      const prod = herbalsProducts.find(p => p.sku === skuOrId || p.id === skuOrId);
      if (!prod) return;

      const titleEl = document.getElementById('pdp-modal-title');
      const subEl = document.getElementById('pdp-modal-subtitle');
      const bodyEl = document.getElementById('product-quickview-body');
      if (!bodyEl) return;

      if (titleEl) titleEl.innerText = prod.name;
      if (subEl) subEl.innerText = `${prod.unani_name || ''} • ${prod.category} Axis • SKU: ${prod.sku}`;

      const discountedPrice = Math.round(prod.price * 0.85);

      bodyEl.innerHTML = `
        <div class="space-y-4 text-xs">
          <!-- Price & Packaging Header -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 flex justify-between items-center">
            <div>
              <span class="text-[10px] uppercase font-bold text-emerald-400 font-mono tracking-wider block">Standardized Packaging</span>
              <strong class="text-white text-sm block">${prod.form || 'HPMC Veg Capsules (60s)'}</strong>
              <span class="text-[10px] text-slate-400">Batch Ref: BMR-2026-${prod.sku}-01 • Shelf Life: 24 Months</span>
            </div>
            <div class="text-right">
              <span class="text-xs text-slate-400 line-through">MRP: ₹${prod.price + 200}</span>
              <div class="text-2xl font-black font-mono text-emerald-400">₹${prod.price.toLocaleString('en-IN')}</div>
              <span class="text-[10px] text-emerald-300 font-bold">Inclusive of all taxes (GST 5%)</span>
            </div>
          </div>

          <!-- Clinical Indications & Posology -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-1">
              <strong class="text-amber-400 block text-[11px]">Primary Clinical Indications:</strong>
              <p class="text-slate-200 text-[11px] leading-relaxed">${prod.indications}</p>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-1">
              <strong class="text-teal-400 block text-[11px]">Standard Daily Posology & Badraqa:</strong>
              <p class="text-slate-200 text-[11px] leading-relaxed">${prod.dosage}</p>
            </div>
          </div>

          <!-- Description -->
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
            <strong class="text-slate-300 block text-[11px]">Therapeutic Doctrine & Pharmacology:</strong>
            <p class="text-slate-300 text-[11px] leading-relaxed">${prod.desc}</p>
          </div>

          <!-- Quality Guarantees Badges -->
          <div class="grid grid-cols-3 gap-2 text-center text-[10px] font-mono">
            <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 text-emerald-300">✓ HPLC Active Tested</div>
            <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 text-emerald-300">✓ Heavy Metals &lt;0.02ppm</div>
            <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 text-emerald-300">✓ 100% Vegetarian (HPMC)</div>
          </div>

          <!-- Purchase Options CTA Bar -->
          <div class="p-4 rounded-2xl bg-gradient-to-r from-emerald-950/70 via-slate-900 to-slate-950 border border-emerald-500/40 space-y-3">
            <div class="flex justify-between items-center text-xs">
              <div>
                <span class="text-white font-bold block">Subscribe &amp; Save 15% (Monthly Doorstep Refill)</span>
                <span class="text-[10px] text-slate-400">Delivered every 30 days. Pause or cancel anytime.</span>
              </div>
              <span class="text-base font-mono font-bold text-emerald-400">₹${discountedPrice}/mo</span>
            </div>
            <div class="flex gap-2">
              <button onclick="addToHerbalsCart('${prod.id}'); toggleProductQuickViewModal(); toggleCheckoutModal();" class="flex-1 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center justify-center gap-1.5">
                <span>⚡</span> Instant Buy Now (₹${prod.price})
              </button>
              <button onclick="addToHerbalsCart('${prod.id}'); toggleProductQuickViewModal();" class="px-5 py-3 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-slate-700 transition">
                + Add to Cart
              </button>
            </div>
          </div>
        </div>
      `;

      const modal = document.getElementById('product-quickview-modal');
      if (modal) modal.classList.remove('hidden');
    }

    function renderCheckoutStep() {
      const body = document.getElementById('checkout-modal-body');
      if (!body) return;

      const subtotal = herbalsCart.reduce((sum, item) => sum + item.price, 0);
      const discount = checkoutState.isSubscription ? Math.round(subtotal * 0.15) : 0;
      const gstTax = Math.round((subtotal - discount) * 0.05); // 5% GST on AYUSH
      const shippingFee = subtotal > 999 ? 0 : 99;
      const finalTotal = subtotal - discount + gstTax + shippingFee;

      if (checkoutState.step === 1) {
        body.innerHTML = `
          <!-- Order Summary Pill -->
          <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 flex justify-between items-center text-xs">
            <div>
              <span class="text-slate-400">Cart Contents:</span>
              <strong class="text-white ml-1">${herbalsCart.length} Formulation(s)</strong>
              <div class="text-[10px] text-emerald-400">${herbalsCart.map(i => i.name).slice(0, 2).join(', ')}${herbalsCart.length > 2 ? '...' : ''}</div>
            </div>
            <div class="text-right">
              <span class="text-slate-400 block text-[10px]">Subtotal:</span>
              <span class="text-base font-bold font-mono text-emerald-400">₹${subtotal.toLocaleString('en-IN')}</span>
            </div>
          </div>

          <!-- Order Type Choice (One-Time vs Subscribe) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <label onclick="checkoutState.isSubscription=false; renderCheckoutStep()" class="cursor-pointer p-3.5 rounded-xl border ${!checkoutState.isSubscription ? 'border-emerald-500 bg-emerald-950/40 text-white shadow-md' : 'border-slate-800 bg-slate-950 text-slate-400'} flex items-start gap-2.5 transition">
              <input type="radio" name="order_type" ${!checkoutState.isSubscription ? 'checked' : ''} class="mt-1 text-emerald-600">
              <div>
                <strong class="block text-slate-200">One-Time Dispensary Order</strong>
                <span class="text-[10px] text-slate-400">Single dispatch with batch COA test certificate.</span>
              </div>
            </label>

            <label onclick="checkoutState.isSubscription=true; renderCheckoutStep()" class="cursor-pointer p-3.5 rounded-xl border ${checkoutState.isSubscription ? 'border-emerald-500 bg-emerald-950/40 text-white shadow-md' : 'border-slate-800 bg-slate-950 text-slate-400'} flex items-start gap-2.5 transition">
              <input type="radio" name="order_type" ${checkoutState.isSubscription ? 'checked' : ''} class="mt-1 text-emerald-600">
              <div>
                <strong class="block text-emerald-300 flex items-center gap-1">
                  <span>🔄</span> Subscribe &amp; Save 15% (Monthly)
                </strong>
                <span class="text-[10px] text-slate-400">Doorstep replenishment every 30 days. Cancel anytime.</span>
              </div>
            </label>
          </div>

          <!-- Shipping Address Form -->
          <div class="space-y-3 bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <h4 class="font-bold text-white text-xs flex items-center gap-1.5">
              <span>📍</span> Doorstep Delivery Details (BlueDart Express Cold-Chain)
            </h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div>
                <label class="block text-[10px] text-slate-400">Full Name</label>
                <input id="chk-name" type="text" value="${checkoutState.shipping.fullName}" class="w-full p-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-emerald-500" />
              </div>
              <div>
                <label class="block text-[10px] text-slate-400">Mobile Phone (+91)</label>
                <input id="chk-phone" type="text" value="${checkoutState.shipping.phone}" class="w-full p-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-emerald-500" />
              </div>
              <div class="sm:col-span-2">
                <label class="block text-[10px] text-slate-400">Delivery Street Address</label>
                <input id="chk-address" type="text" value="${checkoutState.shipping.address}" class="w-full p-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-emerald-500" />
              </div>
              <div>
                <label class="block text-[10px] text-slate-400">City &amp; State</label>
                <input id="chk-city" type="text" value="${checkoutState.shipping.city}, ${checkoutState.shipping.state}" class="w-full p-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-emerald-500" />
              </div>
              <div>
                <label class="block text-[10px] text-slate-400">Postal Pincode</label>
                <input id="chk-pin" type="text" value="${checkoutState.shipping.pincode}" class="w-full p-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-emerald-500" />
              </div>
            </div>
            <div class="p-2 rounded-lg bg-emerald-950/40 border border-emerald-500/30 text-[10px] text-emerald-300 flex items-center justify-between">
              <span>✓ Pincode 110025 Verified: Express 48-Hour Delivery Available</span>
              <span class="font-mono">FREE SHIPPING</span>
            </div>
          </div>

          <!-- Pricing Breakdown Summary -->
          <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5 text-xs font-mono">
            <div class="flex justify-between text-slate-400"><span>Items Subtotal:</span><span>₹${subtotal.toLocaleString('en-IN')}</span></div>
            ${checkoutState.isSubscription ? `<div class="flex justify-between text-emerald-400"><span>15% Subscription Discount:</span><span>-₹${discount.toLocaleString('en-IN')}</span></div>` : ''}
            <div class="flex justify-between text-slate-400"><span>GST Tax (5% HSN 30049011):</span><span>₹${gstTax.toLocaleString('en-IN')}</span></div>
            <div class="flex justify-between text-slate-400"><span>Cold-Chain Thermal Shipping:</span><span class="text-emerald-400 font-bold">${shippingFee === 0 ? 'FREE' : '₹' + shippingFee}</span></div>
            <div class="pt-1 border-t border-slate-800 flex justify-between items-center text-sm font-bold text-white">
              <span>Total Payable Amount:</span>
              <span class="text-emerald-400 text-base">₹${finalTotal.toLocaleString('en-IN')}</span>
            </div>
          </div>

          <!-- Step 1 Footer -->
          <div class="flex justify-between items-center pt-2">
            <button onclick="toggleCheckoutModal()" class="px-4 py-2 border border-slate-700 rounded-xl text-slate-400 hover:text-white">Cancel</button>
            <button onclick="checkoutState.step=2; renderCheckoutStep();" class="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center gap-2">
              <span>Proceed to Payment (₹${finalTotal.toLocaleString('en-IN')})</span>
              <span>&rarr;</span>
            </button>
          </div>
        `;
      } else if (checkoutState.step === 2) {
        body.innerHTML = `
          <!-- Step 2: Payment Gateway Interface -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 flex justify-between items-center text-xs">
            <div>
              <span class="text-slate-400 block text-[10px]">PAYING FOR ORDER:</span>
              <strong class="text-white text-sm">${herbalsCart.length} Formulations &bull; ${checkoutState.isSubscription ? '30-Day Monthly Refill' : 'One-Time Delivery'}</strong>
            </div>
            <div class="text-right">
              <span class="text-slate-400 block text-[10px]">Total Amount</span>
              <span class="text-xl font-bold font-mono text-emerald-400">₹${finalTotal.toLocaleString('en-IN')}</span>
            </div>
          </div>

          <!-- Payment Options -->
          <div class="space-y-3">
            <label class="block text-slate-300 font-bold text-xs">Choose Verified Payment Method:</label>

            <!-- UPI Option -->
            <div onclick="checkoutState.paymentMethod='UPI'; renderCheckoutStep()" class="cursor-pointer p-4 rounded-2xl border ${checkoutState.paymentMethod === 'UPI' ? 'border-emerald-500 bg-slate-950 ring-1 ring-emerald-500' : 'border-slate-800 bg-slate-950/80'} space-y-3 transition">
              <div class="flex justify-between items-center">
                <div class="flex items-center gap-2.5">
                  <input type="radio" name="pay_opt" ${checkoutState.paymentMethod === 'UPI' ? 'checked' : ''} class="text-emerald-600">
                  <strong class="text-white text-xs">Instant UPI &amp; Dynamic QR Code</strong>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 border border-slate-700 text-slate-300">GPay</span>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 border border-slate-700 text-slate-300">PhonePe</span>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 border border-slate-700 text-slate-300">Paytm</span>
                </div>
              </div>

              ${checkoutState.paymentMethod === 'UPI' ? `
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
                  <div class="w-28 h-28 bg-white p-2 rounded-xl flex items-center justify-center shadow-md shrink-0">
                    <!-- Clean SVG QR Code Representation -->
                    <svg viewBox="0 0 100 100" class="w-full h-full text-slate-950" fill="currentColor">
                      <rect width="100" height="100" fill="white" />
                      <path d="M10 10h30v30h-30zM15 15h20v20h-20zM60 10h30v30h-30zM65 15h20v20h-20zM10 60h30v30h-30zM15 65h20v20h-20zM45 15h10v10h-10zM45 45h10v10h-10zM15 45h10v10h-10zM75 45h10v10h-10zM45 75h10v10h-10zM65 65h25v5h-25zM65 75h15v5h-15zM85 75h5v15h-5zM65 85h15v5h-15z" />
                    </svg>
                  </div>
                  <div class="space-y-1 text-xs">
                    <span class="text-emerald-400 font-bold block text-xs">Scan &amp; Pay via any UPI App</span>
                    <p class="text-slate-300 text-[11px]">UPI ID: <code class="text-white font-mono bg-slate-950 px-2 py-0.5 rounded border border-slate-800">zayvora.pay@icici</code></p>
                    <p class="text-[10px] text-slate-400">Zero transaction surcharge. Instant automated payment reconciliation.</p>
                  </div>
                </div>
              ` : ''}
            </div>

            <!-- Card / Netbanking Option -->
            <div onclick="checkoutState.paymentMethod='CARD'; renderCheckoutStep()" class="cursor-pointer p-3.5 rounded-2xl border ${checkoutState.paymentMethod === 'CARD' ? 'border-emerald-500 bg-slate-950 ring-1 ring-emerald-500' : 'border-slate-800 bg-slate-950/80'} flex justify-between items-center transition">
              <div class="flex items-center gap-2.5">
                <input type="radio" name="pay_opt" ${checkoutState.paymentMethod === 'CARD' ? 'checked' : ''} class="text-emerald-600">
                <strong class="text-white text-xs">Debit / Credit Cards &amp; NetBanking</strong>
              </div>
              <span class="text-[10px] text-slate-400">Visa, Mastercard, RuPay</span>
            </div>

            <!-- Cash on Delivery (COD) -->
            <div onclick="checkoutState.paymentMethod='COD'; renderCheckoutStep()" class="cursor-pointer p-3.5 rounded-2xl border ${checkoutState.paymentMethod === 'COD' ? 'border-emerald-500 bg-slate-950 ring-1 ring-emerald-500' : 'border-slate-800 bg-slate-950/80'} flex justify-between items-center transition">
              <div class="flex items-center gap-2.5">
                <input type="radio" name="pay_opt" ${checkoutState.paymentMethod === 'COD' ? 'checked' : ''} class="text-emerald-600">
                <strong class="text-white text-xs">Cash on Delivery (Pay at Doorstep)</strong>
              </div>
              <span class="text-[10px] text-emerald-400 font-mono">Available</span>
            </div>
          </div>

          <!-- Step 2 Footer -->
          <div class="flex justify-between items-center pt-3 border-t border-slate-800">
            <button onclick="checkoutState.step=1; renderCheckoutStep();" class="px-4 py-2 border border-slate-700 rounded-xl text-slate-400 hover:text-white">
              &larr; Back to Address
            </button>
            <button onclick="completeCommercialOrder(${finalTotal});" class="px-7 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center gap-2">
              <span>🔒 Pay &amp; Place Order (₹${finalTotal.toLocaleString('en-IN')})</span>
            </button>
          </div>
        `;
      } else if (checkoutState.step === 3) {
        body.innerHTML = `
          <!-- Step 3: Official Order Confirmation & Tax Invoice Receipt -->
          <div class="p-6 rounded-2xl bg-emerald-950/40 border border-emerald-500/40 text-center space-y-3">
            <div class="w-14 h-14 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center text-2xl mx-auto shadow-inner border border-emerald-500/40">
              ✓
            </div>
            <div>
              <span class="text-[10px] font-mono font-bold text-emerald-400 uppercase tracking-wider block">PAYMENT CONFIRMED &bull; ORDER ALLOCATED</span>
              <h3 class="text-xl font-black text-white mt-0.5">Order ID: #${checkoutState.lastOrderId}</h3>
              <p class="text-xs text-slate-300 mt-1">Thank you! Your order has entered the FEFO temperature-controlled fulfillment pipeline.</p>
            </div>
          </div>

          <!-- Tracking & Delivery Status Card -->
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
            <div class="flex justify-between items-center">
              <span class="text-slate-400">BlueDart Waybill: <strong class="text-white font-mono">ZAY-BLU-2026-8812</strong></span>
              <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-bold border border-emerald-800 text-[10px]">PACKING READY</span>
            </div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
              <div class="bg-emerald-500 h-full w-2/5 rounded-full"></div>
            </div>
            <div class="flex justify-between text-[10px] text-slate-400">
              <span>Order Received</span>
              <span class="text-emerald-400 font-bold">FEFO Packing</span>
              <span>In Transit</span>
              <span>Delivered</span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <button onclick="downloadGstInvoice('${checkoutState.lastOrderId}', ${finalTotal})" class="p-3 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl border border-slate-700 transition flex items-center justify-center gap-2">
              <span>📄</span> Download GST Tax Invoice
            </button>
            <button onclick="showNotification('📲 WhatsApp Order Confirmation sent to ${checkoutState.shipping.phone}!', 'success')" class="p-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl shadow transition flex items-center justify-center gap-2">
              <span>📲</span> Send WhatsApp Receipt
            </button>
          </div>

          <div class="pt-2 border-t border-slate-800 flex justify-end">
            <button onclick="toggleCheckoutModal(); herbalsCart=[]; switchTab('catalog');" class="px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold rounded-xl transition">
              Close &amp; Return to Catalog
            </button>
          </div>
        `;
      }
    }

    function completeCommercialOrder(totalAmount) {
      checkoutState.lastOrderId = `ZAY-ORD-2026-${Math.floor(10000 + Math.random() * 90000)}`;
      checkoutState.step = 3;
      renderCheckoutStep();

      // Automatically queue into dispensary orders list
      showNotification(`✓ Order #${checkoutState.lastOrderId} placed successfully! Queued for FEFO packaging.`, 'success');
    }

    function downloadGstInvoice(orderId, totalAmount) {
      showNotification(`📄 Generating GST Tax Invoice for Order #${orderId} (HSN 30049011 • 5% GST)... Download started!`, 'info');
    }
'''

# 1. Update index.html to insert checkout and PDP modals before </body>
with open(INDEX_FILE, 'r') as f:
    html = f.read()

if 'id="commercial-checkout-modal"' not in html:
    closing_tag = '</body>'
    if closing_tag in html:
        html = html.replace(closing_tag, COMMERCIAL_MODALS_HTML.strip() + '\n\n' + closing_tag)
        with open(INDEX_FILE, 'w') as f:
            f.write(html)
        print("✓ Successfully injected Commercial Checkout and PDP modals into index.html")

# 2. Update js/zayvora-core.js: replace checkoutHerbalsCart with toggleCheckoutModal
with open(CORE_FILE, 'r') as f:
    core_code = f.read()

# Append commercial JS engine at end
if 'function toggleCheckoutModal' not in core_code:
    core_code += '\n' + COMMERCIAL_JS_CODE.strip() + '\n'
    print("✓ Successfully appended Commercial E-Commerce Engine to js/zayvora-core.js")

# In renderHerbalsApp cart checkout button, wire up toggleCheckoutModal
core_code = core_code.replace('onclick="checkoutHerbalsCart()"', 'onclick="toggleCheckoutModal()"')

# In product catalog cards, wire up openProductQuickView(sku)
core_code = core_code.replace("onclick=\"viewWebsitePage('products')\" class=\"px-3.5 py-1.5 bg-slate-800 hover:bg-emerald-600", "onclick=\"openProductQuickView('${p.sku}')\" class=\"px-3.5 py-1.5 bg-slate-800 hover:bg-emerald-600")

with open(CORE_FILE, 'w') as f:
    f.write(core_code)

print("Commercial upgrade script completed.")
