import tkinter as tk
from tkinter import messagebox


# ================= PRODUCT CLASSES =================

class Product:
    def __init__(self, product_id, name, price, quantity):
        self._id = product_id
        self._name = name
        self._price = price
        self._quantity = quantity

    def decrease_quantity(self, qty):
        if qty > 0 and self._quantity >= qty:
            self._quantity -= qty
            return True
        return False

    def increase_quantity(self, qty):
        self._quantity += qty

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_quantity(self):
        return self._quantity

    def display(self):
        return f"{self._id} | {self._name} | ₹{self._price} | Stock: {self._quantity}"


class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, quantity, weight):
        super().__init__(product_id, name, price, quantity)
        self._weight = weight


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, quantity, link):
        super().__init__(product_id, name, price, quantity)
        self._link = link


# ================= CART ITEM =================

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def subtotal(self):
        return self.product.get_price() * self.quantity


# ================= SHOPPING CART =================

class ShoppingCart:
    def __init__(self):
        self.items = {}

        self.catalog = {
            "p001": PhysicalProduct("p001", "T-Shirt", 499, 50, 0.2),
            "p002": PhysicalProduct("p002", "Coffee Mug", 249, 30, 0.4),
            "d001": DigitalProduct("d001", "E-Book", 1299, 1000, "link")
        }

    def add_item(self, pid, qty):
        if pid in self.catalog:
            product = self.catalog[pid]
            if product.decrease_quantity(qty):
                if pid in self.items:
                    self.items[pid].quantity += qty
                else:
                    self.items[pid] = CartItem(product, qty)
                return True
        return False

    def remove_item(self, pid):
        if pid in self.items:
            item = self.items[pid]
            item.product.increase_quantity(item.quantity)
            del self.items[pid]

    def total(self):
        return sum(item.subtotal() for item in self.items.values())


# ================= GUI =================

class ShoppingCartGUI:
    def __init__(self, root):
        self.cart = ShoppingCart()
        self.root = root
        self.root.title("Online Shopping Cart")
        self.root.geometry("650x450")

        tk.Label(root, text="Online Shopping Cart", font=("Arial", 18, "bold")).pack(pady=10)

        self.product_list = tk.Listbox(root, width=80)
        self.product_list.pack()
        self.load_products()

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Product ID").grid(row=0, column=0)
        self.pid_entry = tk.Entry(frame)
        self.pid_entry.grid(row=0, column=1)

        tk.Label(frame, text="Quantity").grid(row=0, column=2)
        self.qty_entry = tk.Entry(frame)
        self.qty_entry.grid(row=0, column=3)

        tk.Button(root, text="Add to Cart", command=self.add_to_cart).pack(pady=5)
        tk.Button(root, text="View Cart", command=self.view_cart).pack(pady=5)
        tk.Button(root, text="Checkout", command=self.checkout).pack(pady=5)

    def load_products(self):
        self.product_list.delete(0, tk.END)
        for p in self.cart.catalog.values():
            self.product_list.insert(tk.END, p.display())

    def add_to_cart(self):
        pid = self.pid_entry.get()
        try:
            qty = int(self.qty_entry.get())
        except:
            messagebox.showerror("Error", "Invalid quantity")
            return

        if self.cart.add_item(pid, qty):
            messagebox.showinfo("Success", "Item added to cart")
            self.load_products()
        else:
            messagebox.showerror("Error", "Failed to add item")

    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Your Cart")

        total = 0
        for item in self.cart.items.values():
            text = f"{item.product.get_name()} | Qty: {item.quantity} | Subtotal: ₹{item.subtotal()}"
            tk.Label(cart_window, text=text).pack()
            total += item.subtotal()

        tk.Label(cart_window, text=f"\nGrand Total: ₹{total}", font=("Arial", 12, "bold")).pack()

    def checkout(self):
        if not self.cart.items:
            messagebox.showwarning("Warning", "Cart is empty")
            return

        messagebox.showinfo("Checkout", f"Total Amount: ₹{self.cart.total()}\nThank you!")
        self.cart.items.clear()


# ================= RUN =================

if __name__ == "__main__":
    root = tk.Tk()
    ShoppingCartGUI(root)
    root.mainloop()
