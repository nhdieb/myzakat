from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    current_app,
)
from flask_mail import Message
from sqlalchemy import func
from datetime import datetime

from app import db, mail
from app.models import ContactSubmission, Donation, Event, Story, PressRelease


from . import main_bp  # ✅ import the blueprint from this folder

# Home route


@main_bp.route("/")
def home():
    total_donations = db.session.query(func.sum(Donation.amount)).scalar() or 0
    total_ramadan_donations = (
        db.session.query(func.sum(Donation.amount))
        .filter(Donation.frequency == "Ramadan")
        .scalar()
        or 0
    )

    meals_budget = total_donations * 0.20
    families_budget = total_donations * 0.50
    orphans_budget = total_donations * 0.30

    # Unit costs
    meal_cost = 5
    family_cost = 100
    orphan_cost = 100
    total_ramadan_donations = 50000

    # Quantities
    meals = int(meals_budget // meal_cost)
    families = int(families_budget // family_cost)
    orphans = int(orphans_budget // orphan_cost)

    events = Event.query.order_by(Event.date.desc()).limit(3).all()  # optional limit

    press_releases = (
        PressRelease.query.order_by(PressRelease.date_posted.desc()).limit(3).all()
    )

    featured_stories = (
        Story.query.filter_by(is_active=True, is_featured=True)
        .order_by(Story.id.desc())
        .limit(5)
        .all()
    )

    if not featured_stories:
        fallback_stories = (
            Story.query.filter_by(is_active=True)
            .order_by(Story.id.desc())
            .limit(5)
            .all()
        )
        story_slides = [
            {
                "image": url_for(
                    "static", filename="images/stories/" + s.image_filename
                ),
                "alt": s.title,
                "text": s.title + ": " + s.summary[:100] + "...",
            }
            for s in fallback_stories
        ]
    else:
        story_slides = [
            {
                "image": url_for(
                    "static", filename="images/stories/" + s.image_filename
                ),
                "alt": s.title,
                "text": s.title + ": " + s.summary[:100] + "...",
            }
            for s in featured_stories
        ]

    now = datetime.utcnow()

    recent_donations = (
        Donation.query.order_by(Donation.donated_at.desc()).limit(5).all()
    )

    testimonials = []
    try:
        from app.models import Testimonial

        testimonials = (
            Testimonial.query.filter_by(is_approved=True)
            .order_by(Testimonial.created_at.desc())
            .limit(3)
            .all()
        )
    except Exception:
        pass

    return render_template(
        "main/home.html",
        total_donations=total_donations,
        total_ramadan_donations=total_ramadan_donations,
        meals=meals,
        families=families,
        orphans=orphans,
        events=events,
        press_releases=press_releases,
        story_slides=story_slides,
        now=now,
        recent_donations=recent_donations,
        testimonials=testimonials,
    )


# About route
@main_bp.route("/about")
def about():
    return render_template("main/about.html")


# Contact route
@main_bp.route("/contact")
def contact():
    return render_template("main/contact.html")


@main_bp.route("/contact-confirmation")
def contact_confirmation():
    return render_template("main/contact_confirmation.html")


# In main/routes.py
@main_bp.route("/stories")
def stories():
    stories = Story.query.filter_by(is_active=True).order_by(Story.id.desc()).all()
    featured = Story.query.filter_by(is_active=True, is_featured=True).limit(1).all()
    return render_template("main/stories.html", stories=stories, featured=featured)


@main_bp.route("/press")
def press():
    all_press = PressRelease.query.order_by(PressRelease.date_posted.desc()).all()
    return render_template("main/press.html", press_list=all_press)


@main_bp.route("/press/<int:press_id>")
def press_detail(press_id):
    press = PressRelease.query.get_or_404(press_id)
    return render_template("main/press_detail.html", press=press)


@main_bp.route("/stories/<int:story_id>")
def story_detail(story_id):
    story = Story.query.get_or_404(story_id)
    return render_template("main/story_detail.html", story=story)


@main_bp.route("/submit-contact", methods=["POST"])
def submit_contact():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("All fields are required!", "error")
            return redirect(url_for("main/contact"))

        new_submission = ContactSubmission(name=name, email=email, message=message)
        db.session.add(new_submission)
        db.session.commit()

        msg = Message(
            "Thanks for Contacting Myzakat.org",
            sender="nhdieb@gmail.com",
            recipients=[email],
        )
        msg.body = f"Dear {name},\n\nThank you for your contacting us. We appreciate your support!\n\nBest regards,\nMyZakat Team"
        mail.send(msg)

        # flash("Thank you for reaching out! Your message has been received.")
        return redirect(url_for("main.contact_confirmation"))

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for("main.contact"))


@main_bp.route("/donate", methods=["GET", "POST"])
def donate():
    zakat_amount = request.args.get("zakat_amount", 0, type=float)
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        amount = request.form.get("amount")
        frequency = request.form.get("frequency", "One-Time")

        # Store the donation in the database (optional)
        donation = Donation(name=name, email=email, amount=amount, frequency=frequency)
        db.session.add(donation)
        db.session.commit()

        msg = Message(
            "Donation Received", sender="nhdieb@gmail.com", recipients=[email]
        )
        msg.body = f"Dear {name},\n\nThank you for your donation of ${amount}. We appreciate your support!\n\nBest regards,\nMyZakat Team"
        mail.send(msg)

        # Redirect to a confirmation page
        flash(
            f"Thank you for your {frequency} donation of {amount} currency units!",
            "success",
        )
        return redirect(url_for("main.donate_confirmation"))

    return render_template("main/donate.html", zakat_amount=zakat_amount)


@main_bp.route("/donate-confirmation")
def donate_confirmation():
    name = request.args.get("name", "Donor")
    amount = float(request.args.get("amount", "0"))
    return render_template("main/donate_confirmation.html", name=name, amount=amount)


# Zakat Calculator
@main_bp.route("/zakat-calculator", methods=["GET", "POST"])
def zakat_calculator():
    zakat_results = {}
    if request.method == "POST":
        total_wealth = request.form.get("total_wealth", type=float)
        liabilities = request.form.get("liabilities", type=float)
        gold_weight = request.form.get("gold_weight", type=float)
        gold_price_per_gram = request.form.get("gold_price_per_gram", type=float)
        silver_weight = request.form.get("silver_weight", type=float)
        silver_price_per_gram = request.form.get("silver_price_per_gram", type=float)
        business_goods = request.form.get("business_goods", type=float)
        agriculture_value = request.form.get("agriculture_value", type=float)

        zakat_results["wealth"] = (
            max(total_wealth - liabilities, 0) * 0.025
            if total_wealth and liabilities
            else 0
        )
        zakat_results["gold"] = (
            gold_weight * gold_price_per_gram * 0.025
            if gold_weight and gold_price_per_gram
            else 0
        )
        zakat_results["silver"] = (
            silver_weight * silver_price_per_gram * 0.025
            if silver_weight and silver_price_per_gram
            else 0
        )
        zakat_results["business_goods"] = (
            business_goods * 0.025 if business_goods else 0
        )
        zakat_results["agriculture"] = (
            agriculture_value * 0.05 if agriculture_value else 0
        )
        zakat_results["total"] = sum(zakat_results.values())

    return render_template("main/zakat_calculator.html", zakat_results=zakat_results)


# Zakat Education route
@main_bp.route("/zakat-education")
def zakat_education():
    return render_template("main/zakat_education.html")


# Newsletter subscription
@main_bp.route("/subscribe_newsletter", methods=["POST"])
def subscribe_newsletter():
    email = request.form.get("email")
    if email:
        flash("Thank you for subscribing to our newsletter!", "success")
        msg = Message(
            "Newsletter Subscription", sender="nhdieb@gmail.com", recipients=[email]
        )
        msg.body = f"Dear subscriber,\n\nThank you for your interest in myZakat.org. We appreciate your support! we will start sending you our newsletter to your email\n\nBest regards,\nMyZakat Team"
        mail.send(msg)
    else:
        flash("Please enter a valid email address.", "error")
    return redirect(url_for("main.home"))


from app.models import Volunteer  # add this import


@main_bp.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        interest = request.form.get("interest")

        if not name or not email or not interest:
            flash("All fields are required!", "error")
            return redirect(url_for("main.volunteer"))

        new_volunteer = Volunteer(name=name, email=email, interest=interest)
        db.session.add(new_volunteer)
        db.session.commit()

        # Send confirmation email
        msg = Message(
            "Thank You for Volunteering!", sender="nhdieb@gmail.com", recipients=[email]
        )
        msg.body = f"""Dear {name},

Thank you for signing up as a volunteer with the Zakat Distribution Foundation.
We are excited to have you join us in the area of: {interest}.

We will be in touch with more details soon.

Warm regards,
MyZakat Team
"""
        mail.send(msg)

        return redirect(url_for("main.volunteer_confirmation", name=name))

    return render_template("main/volunteer.html")


@main_bp.route("/volunteer-confirmation")
def volunteer_confirmation():
    name = request.args.get("name", "Volunteer")
    return render_template("main/volunteer_confirmation.html", name=name)


@main_bp.route("/submit-testimonial", methods=["GET", "POST"])
def submit_testimonial():
    from app.models import Testimonial
    from app.main.forms import TestimonialForm

    form = TestimonialForm()
    if form.validate_on_submit():
        image_filename = None
        video_url = form.video_url.data.strip() if form.video_url.data else None

        # Handle image upload
        if form.image.data:
            image = form.image.data
            if image.filename:
                from werkzeug.utils import secure_filename
                import os

                filename = secure_filename(image.filename)
                image_folder = os.path.join(
                    current_app.root_path, "static", "images", "testimonials"
                )
                os.makedirs(image_folder, exist_ok=True)
                image_path = os.path.join(image_folder, filename)
                image.save(image_path)
                image_filename = f"images/testimonials/{filename}"

        # Handle video upload (optional, if you want to support direct mp4 upload)
        if "video" in request.files and request.files["video"].filename:
            video = request.files["video"]
            from werkzeug.utils import secure_filename
            import os

            video_filename = secure_filename(video.filename)
            video_folder = os.path.join(
                current_app.root_path, "static", "videos", "testimonials"
            )
            os.makedirs(video_folder, exist_ok=True)
            video_path = os.path.join(video_folder, video_filename)
            video.save(video_path)
            video_url = f"videos/testimonials/{video_filename}"

        testimonial = Testimonial(
            name=form.name.data,
            country=form.country.data,
            image=image_filename,
            text=form.text.data,
            rating=form.rating.data,
            video_url=video_url,
            category=form.category.data,
            is_approved=False,
        )
        db.session.add(testimonial)
        db.session.commit()
        flash(
            "Thank you for sharing your story! Your testimonial will be reviewed soon.",
            "success",
        )
        return redirect(url_for("main.home"))
    return render_template("main/submit_testimonial.html", form=form)


@main_bp.route("/programs/<program_slug>")
def program_detail(program_slug):
    # Example program data; in production, fetch from DB or config
    programs = {
        "food-water-aid": {
            "title": "Food & Water Aid",
            "image": "images/program1.jpg",
            "description": "Our Food & Water Aid program delivers essential food parcels and clean water to families in crisis zones. Your support helps us reach the most vulnerable with life-saving resources.",
        },
        "emergency-relief": {
            "title": "Emergency Relief",
            "image": "images/program2.jpg",
            "description": "Our Emergency Relief program provides rapid response for victims of war, disaster, and displacement, offering shelter, supplies, and hope in times of crisis.",
        },
        "orphan-child-care": {
            "title": "Orphan & Child Care",
            "image": "images/program3.jpg",
            "description": "Our Orphan & Child Care program provides education, safety, and hope for orphaned and vulnerable children, ensuring a brighter future for every child.",
        },
    }
    program = programs.get(program_slug)
    if not program:
        return render_template("main/404.html"), 404
    return render_template("main/program_detail.html", program=program)
