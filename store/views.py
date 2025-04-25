from django.shortcuts import render, redirect
from .models import Products
from .forms import ProductForm
import google.generativeai as genai
import requests


GEMINI_API_KEY = 'AIzaSyAD23OTjqg-mfRlNTY9tx8-lt14G9AKPSY'
def generate_tags(product_name, product_description):
    genai.configure(api_key=GEMINI_API_KEY)

    prompt = f"Generate relevant and concise tags for the product '{product_name}' based on this description: {product_description}"

    model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-pro", "gemini-1.0-pro", etc.

    response = model.generate_content(prompt)
    print("Raw response text: ", response.text)  # Print raw response to debug

    # Clean the response text
    text = response.text.strip()
    print("Cleaned response text: ", text)  # Print cleaned response text

    # Clean and split the tags based on commas
    tags = [tag.strip(' *') for tag in text.split(',') if tag.strip()]

    # Print final cleaned tags
    print("Cleaned tags: ", tags)

    return tags

import ast

def product_list(request):
    products = Products.objects.all()

    # Convert the string representation of the tags into an actual list
    for product in products:
        if isinstance(product.tags, str):
            try:
                product.tags = ast.literal_eval(product.tags)  # Safely convert string to list
            except (ValueError, SyntaxError):
                product.tags = []  # Handle case where conversion fails
    
    return render(request, 'store/product_list.html', {'products': products})




def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():

            product_name = form.cleaned_data['name']
            product_description = form.cleaned_data['description']

            tags = generate_tags(product_name, product_description)

            product = form.save(commit=False)
            product.tags = tags
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})