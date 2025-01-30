import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO


class RecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Recommendation System")
        self.root.geometry("800x600")
        
        # User ID Entry
        self.label = tk.Label(root, text="Enter User ID:", font=("Arial", 14))
        self.label.pack(pady=10)
        self.user_id_entry = tk.Entry(root, font=("Arial", 14), width=40)
        self.user_id_entry.pack(pady=10)

        # Get Recommendations Button
        self.get_recommendations_button = tk.Button(
            root, text="Get Recommendations", font=("Arial", 14), bg="blue", fg="white", command=self.fetch_recommendations
        )
        self.get_recommendations_button.pack(pady=20)

        # Recommendation Results Frame
        self.results_frame = tk.Frame(root)
        self.results_frame.pack(fill=tk.BOTH, expand=True)

    def fetch_recommendations(self):
        user_id = self.user_id_entry.get()
        if not user_id:
            messagebox.showerror("Error", "User ID cannot be empty!")
            return

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        try:
            # Fetch recommendations from the API
            response = requests.post(f"http://127.0.0.1:6050/recommend/{user_id}")
            response.raise_for_status()
            recommendations = response.json()

            # Display recommendations
            for product in recommendations:
                self.display_product(product)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch recommendations: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def display_product(self, product):
        # Create a frame for each product
        product_frame = tk.Frame(self.results_frame, pady=10, padx=10, relief=tk.RAISED, bd=2)
        product_frame.pack(fill=tk.X, pady=5)

        # Product Image
        if "image" in product and product["image"]:
            try:
                response = requests.get(product["image"])
                image_data = BytesIO(response.content)
                image = Image.open(image_data).resize((100, 100), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)

                image_label = tk.Label(product_frame, image=photo)
                image_label.image = photo  # Keep reference to avoid garbage collection
                image_label.pack(side=tk.LEFT, padx=10)
            except Exception as e:
                print(f"Error loading image: {e}")

        # Product Details
        details_frame = tk.Frame(product_frame)
        details_frame.pack(side=tk.LEFT, padx=10)

        name_label = tk.Label(details_frame, text=f"Name: {product['name']}", font=("Arial", 12, "bold"))
        name_label.pack(anchor="w")

        desc_label = tk.Label(details_frame, text=f"Description: {product['desc']}", font=("Arial", 10))
        desc_label.pack(anchor="w")

        price_label = tk.Label(details_frame, text=f"Price: ${product['price']}", font=("Arial", 10, "bold"))
        price_label.pack(anchor="w")


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = RecommendationApp(root)
    root.mainloop()
