from pyscript import display, document, HTML  # type: ignore
from html import escape

def SKU_generator(e):
    category = document.getElementById("category").value
    product_name = document.getElementById("product_name").value.strip()
    shoe_size = document.getElementById("shoe_size").value
    stock_qty = document.getElementById("quantity").value

    if not product_name or not shoe_size or not stock_qty:
        display (
            HTML (
                '<div class ="alert alert-warning text-center mb-0">' 
                '<i class = "fa-solid fa-triangle-exclamation me-1"></i>'
                "Please fill in the shoe model, size, and quantity by pairs."
                "</div>"
            ),
            target = "sku_output",
            append = False,

        )
        return
    model_code = product_name.replace(" ","")[:4].upper()
    size = float(shoe_size)
    size_code = str(int(size)) if size % 1 == 0 else str(size)
    sku = f"{category}-{model_code}-{size_code}-{stock_qty}"

    display (
        HTML (
            f'<p class="small mb-1">Generated SKU</p>'
            f'<div class="sku-code">{escape(sku)}</div>'
            f'<p class="small mt-2 mb-0">{escape(product_name)}'
            f"Size US{escape(shoe_size)} ; Qty {escape(stock_qty)}</p>"
        ),
        target="sku_output",
        append=False

    )

def create_order(e) :
    prod1 = document.getElementById("item1")
    prod2 = document.getElementById("item2")
    prod3 = document.getElementById("item3")
    prod4 = document.getElementById("item4")
    prod5 = document.getElementById("item5")
    prod6 = document.getElementById("item6")

    subtotal = (
    + float(prod1.value) * prod1.checked
    + float(prod2.value) * prod2.checked
    + float(prod3.value) * prod3.checked
    + float(prod4.value) * prod4.checked
    + float(prod5.value) * prod5.checked
    + float(prod6.value) * prod6.checked
    )

    tax_rate = 0.12
    tax = subtotal * tax_rate
    total = subtotal + tax

    receipt = f"""
    <h3>==== Receipt ====</h3>
    <p>Subtotal: ₱{subtotal:.2f}</p>
    <p>Tax (12%): ₱{tax:.2f}</p>
    <p>Total: ₱{total:.2f}</p>
    <p><strong>Total: ₱{total:.2f}</strong></p>
    """
    document.getElementById("show").innerHTML = receipt


def clear_order(e):
    for i in range(1, 7):
        document.getElementById(f"item{i}").checked = False
        document.getElementById("show").innerHTML = '<p class="text-muted text-center mb-0">Your receipt will appear here.</p>'