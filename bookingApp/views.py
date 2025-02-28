from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.templatetags.static import static
import stripe
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime
from .models import Room, Reservation
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, "home.html")

#Rooms details
ROOMS = {
  101: {
    'name': "Deluxe Triple Room 101",
    'size': "<b>Size:</b> 35 m² <br /> 1 sofa bed🛋️ and 1 large double bed🛏️",
    'description':
      "Meals can be prepared in the kitchenette, which comes with a stovetop, a refrigerator, kitchenware and a tea and coffee maker. The spacious triple room provides air conditioning, a private entrance, a terrace with sea views as well as a private bathroom featuring a shower. The unit offers 2 beds.",
    'price': "65€",
    'gallery': [
      "101_1.jpeg",
      "101_2.jpeg",
      "101_3.jpeg",
      "101_4.jpeg",
      "101_5.jpeg",
    ],
    'bckgImage': "101_1.jpeg",
  },
  102: {
    'name': "Apartment with View 102",
    'size': "<b>Size:</b> 65 m² <br /> 2 sofa beds🛋️ and 1 large double bed🛏️",
    'description':
      "Boasting a private entrance, this air-conditioned apartment comes with 1 living room, 1 separate bedroom and 1 bathroom with a shower and a hairdryer. A kitchenette fitted with a stovetop, a refrigerator and kitchenware is available for cooking and storing food. The spacious apartment features a washing machine, soundproof walls, a tea and coffee maker as well as a terrace with sea views. The unit has 3 beds.",
    'price': "80€",
    'gallery': [
      "102_1.jpeg",
      "102_2.jpeg",
      "102_3.jpeg",
      "102_4.jpeg",
      "102_5.jpeg",
      "102_6.jpeg",
    ],
    'bckgImage': "102_1.jpeg",
  },
  103: {
    'name': "Apartment with View 103",
    'size': "<b>Size:</b> 70 m² <br /> 2 sofa beds🛋️ and 1 large double bed🛏️",
    'description':
      "Featuring a private entrance, this air-conditioned apartment comprises 1 living room, 1 separate bedroom and 1 bathroom with a shower and a hairdryer. Meals can be prepared in the kitchen, which comes with a stovetop,an oven, a refrigerator, a dishwasher and kitchenware. The spacious apartment provides a washing machine, soundproof walls, a tea and coffee maker as well as a terrace with sea views. The unit offers 3 beds.",
    'price': "85€",
    'gallery': [
      "103_1.jpeg",
      "103_2.jpeg",
      "103_3.jpeg",
      "103_4.jpeg",
      "103_5.jpeg",
      "103_6.jpeg",
    ],
    'bckgImage': "103_1.jpeg",
  },
  104: {
    'name': "Deluxe Triple Room 104",
    'size': "<b>Size:</b> 35 m² <br /> 1 sofa bed🛋️ and 1 large double bed🛏️",
    'description':
      "In the fully equipped kitchenette, guests will find a stovetop, a refrigerator, kitchenware and a tea and coffee maker. The spacious triple room offers air conditioning, a private entrance, a terrace with sea views as well as a private bathroom boasting a shower. The unit has 2 beds.",
    'price': "65€",
    'gallery': [
      "104_1.jpeg",
      "104_2.jpeg",
      "104_3.jpeg",
      "104_4.jpeg",
      "104_5.jpeg",
    ],
    'bckgImage': "104_1.jpeg",
  },
  105: {
    'name': "Deluxe Triple Room 105",
    'size': "<b>Size:</b> 35 m² <br /> 1 sofa bed🛋️ and 1 large double bed🛏️",
    'description':
      "Guests can make meals in the kitchenette that comes with a stovetop, a refrigerator, kitchenware and a tea and coffee maker. The spacious triple room provides air conditioning, a private entrance, a terrace with sea views as well as a private bathroom featuring a shower. The unit offers 2 beds.",
    'price': "65€",
    'gallery': ["105_1.jpeg", "105_2.jpeg", "105_3.jpeg", "105_4.jpeg"],
    'bckgImage': "105_1.jpeg",
  },
  106: {
    'name': "Deluxe Triple Room 106",
    'size': "<b>Size:</b> 35 m² <br /> 1 sofa bed🛋️ and 1 large double bed🛏️",
    'description':
      "Guests can make meals in the kitchenette that has a stovetop, a refrigerator, kitchenware and a tea and coffee maker. The spacious triple room features air conditioning, a private entrance, a terrace with sea views as well as a private bathroom boasting a shower. The unit has 2 beds.",
    'price': "70€",
    'gallery': [
      "106_1.jpeg",
      "106_2.jpeg",
      "106_3.jpeg",
      "106_4.jpeg",
      "106_5.jpeg",
    ],
    'bckgImage': "106_1.jpeg",
  },
  107: {
    'name': "Deluxe Triple Room 107",
    'size': "<b>Size:</b> 35 m² <br /> 1 sofa bed🛋️ and 1 large double bed🛏️",
    'description':
      "The well-equipped kitchenette features a stovetop, a refrigerator, kitchenware and a tea and coffee maker. The spacious triple room offers air conditioning, a private entrance, a terrace with sea views as well as a private bathroom featuring a shower. The unit offers 2 beds.",
    'price': "80€",
    'gallery': [
      "107_1.jpeg",
      "107_2.jpeg",
      "107_3.jpeg",
      "107_4.jpeg",
      "107_5.jpeg",
    ],
    'bckgImage': "107_1.jpeg",
  },
  108: {
    'name': "Deluxe Triple Room with Sea View 108",
    'size': "<b>Size:</b> 35 m² <br /> 1 sofa bed 🛋️ and 1 large double bed 🛏️",
    'description':
      "Fully equipped kitchenette with stovetop, refrigerator, kitchenware, and a tea and coffee maker. Air-conditioned room with a private entrance, terrace with sea views, and a private bathroom with a shower.",
    'price': "80€",
    'gallery': [
      "108_1.jpeg",
      "108_2.jpeg",
      "108_3.jpeg",
      "108_4.jpeg",
      "108_5.jpeg",
      "108_6.jpeg",
    ],
    'bckgImage': "108_1.jpeg",
  },
  109: {
    'name': "Deluxe Triple Room with Sea View 109",
    'size': "<b>Size:</b> 35 m² <br /> 1 sofa bed 🛋️ and 1 large double bed 🛏️",
    'description':
      "The well-equipped kitchenette has a stovetop, a refrigerator, kitchenware and a tea and coffee maker. The spacious triple room features air conditioning, a private entrance, a terrace with sea views as well as a private bathroom boasting a shower. The unit has 2 beds.",
    'price': "80€",
    'gallery': [
      "109_1.jpeg",
      "109_2.jpeg",
      "109_3.jpeg",
      "109_4.jpeg",
      "109_5.jpeg",
      "109_6.jpeg",
    ],
    'bckgImage': "109_1.jpeg",
  },
}

def room_detail(request, room_id):
    room = ROOMS.get(room_id)
    
    if not room:
        raise Http404("Room not found")
    
    room["bckgImagePath"] = static(f"dhomat/Room{room_id}/{room['bckgImage']}")
    room["galleryPaths"] = [static(f"dhomat/Room{room_id}/{img}") for img in room["gallery"]]

    return render(request, "rooms.html", {"room": room})

def contactForm(request):
    if request.method == "POST":
        full_name = request.POST.get("fullName")
        email = request.POST.get("email")
        room = request.POST.get("package")
        check_in = request.POST.get("date")
        no_people = request.POST.get("noPeople")
        message = request.POST.get("message")

        # Email for admin
        admin_subject = "New Booking Request"
        admin_message = f"""
        New Booking Request:
        Name: {full_name}
        Email: {email}
        Room: {room}
        Check-in Date: {check_in}
        Number of People: {no_people}
        Message: {message}
        """
        admin_email = "anxhinebi@gmail.com"

        # Email for user
        user_subject = "Booking Confirmation"
        user_message = f"""
        Dear {full_name},

        Thank you for your reservation request at our hotel.
        Here are your booking details:
        • Room:   {room}
        • Check-in Date:   {check_in}
        • Number of People:   {no_people}

        We will contact you shortly to confirm your booking.

        Best Regards,
        Oni Apartments Sarande
        """
        send_mail(admin_subject, admin_message, "anxhinebi@gmail.com", [admin_email])
        send_mail(user_subject, user_message, "nebianxhi@gmail.com", [email])

        return redirect('home')

    return render(request, 'home.html')  
         

def check_availability(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        room = next((r for r in ROOMS.values() if r["name"] == room_name), None)
        if not room:
            print("Room not found!")
            return redirect("home")

        price_per_night = float(room['price'].replace("€", ""))

        existing_bookings = Reservation.objects.filter(room__name=room_name).filter(
            check_in__lt=check_out, check_out__gt=check_in
        )

        if existing_bookings.exists():
            messages.warning(request, "This room is occupied! Please choose another.")
            url = reverse('home')
            return redirect(f'{url}?section=rooms')

        print("Room is available!")
        url = reverse('submit_booking', args=[room_name, check_in, check_out])
        return redirect(f"{url}?price_per_night={price_per_night}")
    return redirect("home")

def submit_booking(request, room_name, check_in_date, check_out_date):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        adults = request.POST.get("adults")
        card_holder = request.POST.get("card_holder")
        card_number = request.POST.get("card_number")
        exp_month = request.POST.get("exp_month")
        exp_year = request.POST.get("exp_year")
        cvv = request.POST.get("cvv")

        room = get_object_or_404(Room, name__iexact=room_name.strip())

        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

        num_nights = (check_out_date - check_in_date).days

        price_per_night = room.price_per_night

        total_price = num_nights * price_per_night
        print(f"Total Price: {total_price}")
        
        reservation = Reservation(
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            full_name=full_name,
            email=email,
            adults=adults,
            total_price=total_price,
            card_holder=card_holder,
            card_number=card_number,
            exp_month=exp_month,
            exp_year=exp_year,
            cvv=cvv
        )
        reservation.save()

        room.is_occupied = True
        room.save()
        
        admin_subject = "New Booking Request"
        admin_message = f"""
        New Booking Request:
        Name:   {full_name}
        Email:   {email}
        Room:   {room}
        Check-in Date:   {check_in}
        Check-out Date:   {check_out}
        Number of People:   {adults}
        Total price:   {total_price}
        """
        admin_email = "anxhinebi@gmail.com"

        # Email for user
        user_subject = "Booking Confirmation"
        user_message = f"""
        Dear {full_name},

        Thank you for your reservation at our hotel.
        Here are your booking details:
        
        • Room:   {room}
        • Check-in Date(y/m/d):   {check_in}
        • Check-out Date(y/m/d):   {check_out}
        • Number of People:   {adults}
        • Total price:   {total_price}

        You have 15 days before {check_in} to cancel your booking via email. After that you will be charged the full price.

        Best Regards,
        Oni Apartments Sarande
        """
        send_mail(admin_subject, admin_message, "anxhinebi@gmail.com", [admin_email])
        send_mail(user_subject, user_message, "nebianxhi@gmail.com", [email])
        messages.success(request, "Thank you for choosing Oni Apartments Sarandë!")

        return redirect("booking_success")

    return render(request, "booking_form.html", {
        "room_name": room_name,
        "check_in": check_in_date,
        "check_out": check_out_date,
        "price_per_night": request.GET.get("price_per_night")
    })        