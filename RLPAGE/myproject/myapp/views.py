from django.shortcuts import render, redirect
from .models import Register,Mobile
from .forms import RegistrationForm
from django.http import JsonResponse
from .scrape import scrape_amazon_product

def first(request):
    return render(request, 'first.html')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            mobile_number = form.cleaned_data.get("mobile_number")  # Retrieve mobile number from the form

            try:
                # Check if username, email, or mobile number already exists in the database
                if Register.objects.filter(username=username).exists():
                    return JsonResponse({"message": "Username already exists."}, status=400)
                if Register.objects.filter(email=email).exists():
                    return JsonResponse({"message": "Email already exists."}, status=400)
                if Register.objects.filter(mobile_number=mobile_number).exists():  # Check mobile number uniqueness
                    return JsonResponse({"message": "Mobile number already exists."}, status=400)
                # Create a new user object and save it to the database
                user = Register.objects.create(username=username, email=email, password=password, mobile_number=mobile_number)
                # Redirect to the login page after successful registration
                 # Set session variable to store the username
                request.session['username'] = username
                request.session['email'] = email  
                request.session['mobile_number'] = mobile_number

                return redirect('login')  # Assuming you have a URL pattern named 'login' for your login page
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)
        else:
            # Return form errors if the form is invalid
            return JsonResponse({"message": form.errors}, status=400)
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not (username and password):
            return JsonResponse({"message": "Please provide both username and password."}, status=400)

        try:
            user = Register.objects.get(username=username, password=password)
            if user:
                # Perform login actions here if needed
                # Set session variable to store the username
                request.session['username'] = username
                # Redirect to profile page after successful login
                return JsonResponse({"message": "Login successful."}, status=200)
            else:
                return JsonResponse({"message": "Invalid username or password."}, status=401)
        except Register.DoesNotExist:
            return JsonResponse({"message": "Invalid username or password."}, status=401)
    else:
        return render(request, 'login.html')

def main(request):
    username = request.session.get('username')
    if username:
        user = Register.objects.get(username=username)
    else:
        return redirect('profile')
    mobiles = Mobile.objects.all()

    # Scrape product prices
    amazon_products_data = []
    

    amazon_urls = [
        'https://amzn.to/3J29J4M',
        'https://amzn.to/3TGXjUO',
        'https://amzn.to/3PHakfY',
        'https://amzn.to/3VFGDQi',
        'https://amzn.to/3xjTn51',
        'https://amzn.to/43CJhbm',
        'https://amzn.to/4cFrKU4',
        'https://amzn.to/43Va96V',
        'https://amzn.to/3VFpjuB',
        'https://amzn.to/3xf6DYL',
        'https://amzn.to/3VHoyRQ',
        'https://amzn.to/3IXwUx5',
        'https://amzn.to/3xeCU1X',
        'https://amzn.to/43NazMw',
        'https://amzn.to/49iaj99',
        'https://amzn.to/4cDeEGS',
        'https://amzn.to/3PJa4wY',
        'https://amzn.to/3TYJ1Am',
        'https://amzn.to/4cFfZx6',
        'https://amzn.to/3VFwiUj',
        'https://amzn.to/3TUxj9T',
        'https://amzn.to/3TGVXcN',
        'https://amzn.to/3PIAVJN',
        'https://amzn.to/49ozFSN',
        'https://amzn.to/3J2iYSs',
        'https://amzn.to/3xk34R3',
        'https://amzn.to/3J0uVZ6',
        'https://amzn.to/3xja4gY',
        'https://amzn.to/4aDJ8GT',
        'https://amzn.to/4aCY8F0',
        'https://amzn.to/3TWfs2t',
        'https://amzn.to/4aAG8LG',
        'https://amzn.to/3VHifh9',
        'https://amzn.to/3vmErmd',
        'https://amzn.to/49gEe1H',
        'https://amzn.to/3x7yJF1',
        'https://amzn.to/3PCJHZO',
        'https://amzn.to/4aaY9An',
        'https://amzn.to/4apijq2',
        'https://amzn.to/3VCFYPq',
        'https://amzn.to/49m4lUJ',
        'https://amzn.to/4adylDB',
        'https://amzn.to/3VEuifc',
        'https://amzn.to/3Vzaqdv',
        'https://amzn.to/3VD2OXt',
        'https://amzn.to/3IZ7Wxy',
        'https://amzn.to/3vn88U9',
        'https://amzn.to/43Bzfas',
        'https://amzn.to/3TAWcpW',
        'https://amzn.to/3TzsG3P',
        'https://amzn.to/3xhC8Br',
        'https://amzn.to/43G1FAg',
        'https://amzn.to/4aw1QjM',
        'https://amzn.to/3PIPgpy',
        'https://amzn.to/3J0tIRj',
        'https://amzn.to/3J15Yg3',
        'https://amzn.to/3PFb31q',
        'https://amzn.to/3J1LWSu',
        'https://amzn.to/49oAk6J',
        'https://amzn.to/49dtGjX',
        'https://amzn.to/4avyjY9',
        'https://amzn.to/3J3szIS',
        'https://amzn.to/43I8tgJ',
        'https://amzn.to/43D2j1r',
        'https://amzn.to/3PIA6R0',
        'https://amzn.to/3vGPVAP',
        'https://amzn.to/3PLjCYu',
        'https://amzn.to/4aBycJX',
        'https://amzn.to/3U0mfIy',
        'https://amzn.to/3VzBKZ4',
        'https://amzn.to/4ahPThS',
        'https://amzn.to/4ajsj4C',
        'https://amzn.to/3VGYjv4',
        'https://amzn.to/3xloPjl',
        'https://amzn.to/3VGVLg9',
        'https://amzn.to/3VGVLg10',
        'https://amzn.to/3VGVLg11',
        'https://amzn.to/3VGVLg12',
        'https://amzn.to/3VGVLg13',
        'https://amzn.to/3VGVLg14',
        'https://amzn.to/3TCRS9u',
        'https://amzn.to/3Vzw950',
        'https://amzn.to/49oCTWp',
        'https://amzn.to/3PFP8XC',
        'https://amzn.to/43Eokge',
        'https://amzn.to/3VCCaxG',
        'https://amzn.to/3VzR9sn',
        'https://amzn.to/49dBC4J',
        'https://amzn.to/3IYCwqY',
        'https://amzn.to/43Nlrdi',
        'https://amzn.to/43GbYo2',
        'https://amzn.to/3PJl8Kw',
        'https://amzn.to/3VGJtEH',
        'https://amzn.to/3VFzcIY',
        'https://amzn.to/3PMpuki',
        'https://amzn.to/4aFiYnv',
        'https://amzn.to/4cBnAN4',
        'https://amzn.to/3TXLI54',
        'https://amzn.to/3PFUSAM',
        'https://amzn.to/3vqHN7I',
        'https://amzn.to/49qTGbK',
        'https://amzn.to/49h7S6T',
        'https://amzn.to/4avXPf6',
        'https://amzn.to/4aA8s0z',
        'https://amzn.to/3vyPl8k',
        'https://amzn.to/3TVJKCi',
        'https://amzn.to/4cFFgXI',
        'https://amzn.to/3U0b6Ye',
        'https://amzn.to/3J135fd',
        'https://amzn.to/3TYGp5D',
        'https://amzn.to/3TVZqFM',
        'https://amzn.to/3xiESyi',
        'https://amzn.to/3vxAawe',
        'https://amzn.to/3J2iFr4',
        'https://amzn.to/3TZ2wZx',
        'https://amzn.to/3TZUYpF',
        'https://amzn.to/4acpphO',
        'https://amzn.to/3PKOAjh',
        'https://amzn.to/3PLgo7n',
        'https://amzn.to/3VB7k8M',
        'https://amzn.to/4avz6IB',
        'https://amzn.to/4aAckP9',
        'https://amzn.to/4aBye4B',
        'https://amzn.to/4al3B3F',
        'https://amzn.to/43EsBQS',
        'https://amzn.to/3PLcTxI',
        'https://amzn.to/4acs2jG',
        'https://amzn.to/4aeeaFO',
        'https://amzn.to/3VBh039',
        'https://amzn.to/49cZS6U',
        'https://amzn.to/43Nhwx6',
        'https://amzn.to/3xiVXIy',
        'https://amzn.to/3vBb7s6',
        'https://amzn.to/3J0wt5m',
        'https://amzn.to/3J1hxnu',
        'https://amzn.to/3TXzhq5',
        'https://amzn.to/3VGO75r',
        'https://amzn.to/4asSp4U',
        'https://amzn.to/43Deyev',
        'https://amzn.to/49ep3G5',
    ]
    
    for url in amazon_urls:
        product_data = scrape_amazon_product(url)
        if product_data:
            amazon_products_data.append(product_data)

    
    # Zip the mobiles with scraped prices
    mobiles_with_prices = zip(mobiles, amazon_products_data, username, user)


    return render(request, 'main.html', {'mobiles_with_prices': mobiles_with_prices})

def profile(request):
    username = request.session.get('username')
    if username:
        try:
            user = Register.objects.get(username=username)
        except Register.MultipleObjectsReturned:
            user = Register.objects.filter(username=username).first()  # Retrieve the first object

        if request.method == "POST":
            new_username = request.POST.get("username")
            user.username = new_username
            user.email = request.POST.get("email")
            user.mobile_number = request.POST.get("mobilenumber")
            
            profile_image = request.FILES.get('image')
            if profile_image:
                user.profile_image = profile_image
            user.save()
            
            # Update session with the new username
            request.session['username'] = new_username
            
            # Redirect back to the main page after saving the profile
            return redirect('main')
        
        return render(request, 'profile.html', {'user': user})
    else:
        return redirect('register')