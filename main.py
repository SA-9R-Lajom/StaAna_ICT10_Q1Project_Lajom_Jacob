from datetime import datetime
import random
 
from pyscript import document #
 
VAT_RATE = 0.12 
MAX_QTY = 5
 
 
def peso(amount):
    return f"₱{amount:,.2f}"
 
 
def get_selected_items():
    
    items = []
    for box in document.querySelectorAll(".item-check"):
        if not box.checked:
            continue
 
        qty_box = document.getElementById(box.getAttribute("data-qty"))
        size_box = document.getElementById("size" + box.id.replace("item", ""))
        label = document.querySelector(f'label[for="{box.id}"]')
 
        # Keep quantity between 1 and MAX_QTY, even if someone types nonsense
        try:
            qty = int(qty_box.value)
        except (ValueError, TypeError):
            qty = 1
        qty = max(1, min(MAX_QTY, qty))
        qty_box.value = qty
 
        price = int(box.value)
        items.append({
            "name": label.textContent.strip(),
            "size": size_box.value,
            "qty": qty,
            "price": price,
            "amount": price * qty,
        })
    return items
 
 
def update_total(event=None):

    for box in document.querySelectorAll(".item-check"):
        qty_box = document.getElementById(box.getAttribute("data-qty"))
        qty_box.disabled = not box.checked
 
    total = sum(item["amount"] for item in get_selected_items())
    document.getElementById("liveTotal").textContent = peso(total)
 
 
def create_order(event):
    output = document.getElementById("show")
    items = get_selected_items()
 
    if not items:
        output.innerHTML = (
            '<div class="alert alert-warning mb-0 text-center">'
            '<i class="fa-solid fa-triangle-exclamation me-1"></i> '
            'Please tick at least one pair of shoes first.</div>'
        )
        return
 
    total = sum(i["amount"] for i in items)
    pairs = sum(i["qty"] for i in items)
    vatable = total / (1 + VAT_RATE)
    vat = total - vatable
 
    now = datetime.now()
    order_no = f"SZ-{now:%y%m%d}-{random.randint(1000, 9999)}"
 
    lines = ""
    for i in items:
        lines += f"""
        <div class="r-line">
            <span><strong>{i['name']}</strong></span>
            <span>{peso(i['amount'])}</span>
        </div>
        <div class="r-line" style="color:#7a746a; font-size:0.78rem;">
            <span>  US {i['size']} &times; {i['qty']} @ {peso(i['price'])}</span>
            <span></span>
        </div>
        """
 
    output.innerHTML = f"""
    <div class="receipt">
        <div class="text-center">
            <h5>SHOEZIFY</h5>
            <div class="r-thanks">Jordan Collection &bull; Official Receipt</div>
        </div>
 
        <div class="r-dash"></div>
        <div class="r-meta"><span>Order No:</span><span>{order_no}</span></div>
        <div class="r-meta"><span>Date:</span><span>{now:%b %d, %Y}</span></div>
        <div class="r-meta"><span>Time:</span><span>{now:%I:%M %p}</span></div>
        <div class="r-dash"></div>
 
        {lines}
 
        <div class="r-dash"></div>
        <div class="r-line"><span>Items</span><span>{len(items)} style(s) / {pairs} pair(s)</span></div>
        <div class="r-line"><span>VATable Sales</span><span>{peso(vatable)}</span></div>
        <div class="r-line"><span>VAT (12%, included)</span><span>{peso(vat)}</span></div>
        <div class="r-line total"><span>TOTAL</span><span>{peso(total)}</span></div>
 
        <div class="r-dash"></div>
        <div class="text-center">
            <div style="font-size:1.4rem; letter-spacing:2px;">&#9646;&#9646;&#9647;&#9646;&#9647;&#9647;&#9646;&#9646;&#9647;&#9646;&#9646;&#9647;&#9646;</div>
            <div class="r-thanks">Thank you for shopping at ShoeZify!<br>Keep your receipt for exchanges within 7 days.</div>
            <button class="btn btn-sm btn-dark mt-3 no-print" onclick="window.print()">
                <i class="fa-solid fa-print me-1"></i> Print Receipt
            </button>
        </div>
    </div>
    """
    output.scrollIntoView({"behavior": "smooth", "block": "nearest"})
 
def clear_order(event):
    for box in document.querySelectorAll(".item-check"):
        box.checked = False
        document.getElementById(box.getAttribute("data-qty")).value = 1
        document.getElementById("size" + box.id.replace("item", "")).value = "10"

    update_total()
    document.getElementById("show").innerHTML = (
        '<p class="text-muted text-center mb-0">Your receipt will appear here.</p>'
    )

def SKU_generator(event):
    category = document.getElementById("category").value
    model = document.getElementById("product_name").value.strip()
    size = document.getElementById("shoe_size").value
    qty = document.getElementById("quantity").value
    output = document.getElementById("sku_output")

    if not model or not size or not qty:
        output.innerHTML = '<p class="mb-0">Please fill in all fields.</p>'
        return

    try:
        qty = int(qty)
        size_num = float(size)
    except ValueError:
        output.innerHTML = '<p class="mb-0">Size and quantity must be numbers.</p>'
        return

    initials = "".join(w[0] for w in model.split() if w[0].isalnum()).upper()
    size_code = f"{size_num:g}".replace(".", "")   # 10.5 -> "105", 9 -> "9"
    sku = f"{category}-{initials}-{size_code}-{qty:03d}"

    output.innerHTML = f'<div class="sku-code">{sku}</div>'