from pyscript import document


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
    size_code = f"{size_num:g}".replace(".", "")
    sku = f"{category}-{initials}-{size_code}-{qty:03d}"

    output.innerHTML = f'<div class="sku-code">{sku}</div>'
