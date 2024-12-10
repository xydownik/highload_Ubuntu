from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from api.models import Product, Category, ShoppingCart, CartItem, Order, OrderItem, Wishlist, WishlistItem, Review

def shop_home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'front/home.html', {'categories': categories, 'products': products})

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category_id=category)
    return render(request, 'front/category.html', {'category': category, 'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'front/products.html', { 'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product_id=product).order_by('-created_at')
    return render(request, 'front/product_detail.html', {'product': product, 'reviews': reviews})

@login_required(login_url='login')
def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'front/cart.html', {'cart': cart, 'total': total})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_price = float(product.price)
    quantity = int(request.POST.get('quantity', 1))

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': product_price,
            'quantity': 1
        }

    request.session['cart'] = cart
    return redirect('view_cart')

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})

    # If the item exists in the cart, remove it
    if str(item_id) in cart:
        del cart[str(item_id)]

    request.session['cart'] = cart
    return redirect('view_cart')

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user_id=request.user)
    return render(request, 'front/orders.html', {'orders': orders})


@login_required(login_url='login')
def view_wishlist(request):
    # Get or create the user's wishlist
    wishlist, _ = Wishlist.objects.get_or_create(user_id=request.user)

    # Fetch all products in the wishlist
    items = WishlistItem.objects.filter(wishlist_id=wishlist)

    # Return the wishlist page with the products
    return render(request, 'front/wishlist.html', {'wishlist': wishlist, 'items': items})

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    # Get or create the user's wishlist
    wishlist, _ = Wishlist.objects.get_or_create(user_id=request.user)

    # Get the product or return 404 if it doesn't exist
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the wishlist
    if not WishlistItem.objects.filter(wishlist_id=wishlist, product_id=product).exists():
        # Create a new WishlistItem
        WishlistItem.objects.create(wishlist_id=wishlist, product_id=product)

    # Redirect to the wishlist view
    return redirect('view_wishlist')


@login_required(login_url='login')
def remove_from_wishlist(request, item_id):
    # Get the WishlistItem object to delete
    item = get_object_or_404(WishlistItem, id=item_id)

    # Delete the item
    item.delete()

    # Redirect to the wishlist view
    return redirect('view_wishlist')


@login_required(login_url='login')
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST['review']
        review = Review.objects.create(
            product_id=product,
            user_id=request.user,
            rating=rating,
            comment=comment
        )
        review.save()
        return redirect('product_detail', product_id=product.id)
    return render(request, 'front/add_review.html', {'product': product})


def home(request):
    return render(request, 'front/home.html')