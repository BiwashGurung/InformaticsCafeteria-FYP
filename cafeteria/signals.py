# cafeteria/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

# Helper function to build email content
def build_email_content(instance, is_creation=False):
    subject = f"Order #{instance.id} Status {'Created' if is_creation else 'Update'}"
    
    # Plain text message
    plain_message = f"Dear {instance.user.username},\n\n"
    if is_creation:
        plain_message += f"Your order #{instance.id} has been successfully placed with status 'Pending'.\n"
    else:
        plain_message += f"Your order #{instance.id} status has been updated to '{instance.status}'.\n"
    
    if instance.status == "Preparing":
        plain_message += "Our chefs are preparing your order. You'll be notified when it's ready!\n"
    elif instance.status == "Completed":
        plain_message += "Your order is ready! Please pick it up or enjoy your dine-in soon.\n"
    elif instance.status == "Cancelled":
        plain_message += "Your order has been cancelled. Contact us at informaticscafetera@gmail.com if this was an error.\n"
    else:  # "Pending"
        plain_message += "Your order status is Pending. We'll keep you posted!\n"
    plain_message += (
        f"\nOrder Details:\n"
        f"- Total: Rs. {instance.total_price}\n"
        f"- Payment: {instance.get_payment_method_display()}\n"
        f"- Date: {instance.order_date.strftime('%Y-%m-%d %H:%M')}\n"
        f"- Items:\n"
    )
    for item in instance.order_items.all():
        plain_message += f"  - {item.food_item.name} (x{item.quantity})\n"
    plain_message += "\nThank you,\nInformatics Cafeteria Team"

    # HTML message
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2 style="color: #2c3e50;">Order #{instance.id} Status {'Created' if is_creation else 'Update'}</h2>
            <p>Dear {instance.user.username},</p>
    """
    if is_creation:
        html_message += f"<p>Your order #{instance.id} has been successfully placed with status <strong style='color: #f1c40f;'>Pending</strong>.</p>"
    else:
        html_message += f"<p>Your order status has been updated to <strong style='color: #e74c3c;'>{instance.status}</strong>.</p>"

    if instance.status == "Preparing":
        html_message += "<p style='color: #e67e22;'>Our chefs are preparing your order. You'll be notified when it's ready!</p>"
    elif instance.status == "Completed":
        html_message += "<p style='color: #27ae60;'>Your order is ready! Please pick it up or enjoy your dine-in soon.</p>"
    elif instance.status == "Cancelled":
        html_message += "<p style='color: #c0392b;'>Your order has been cancelled. Contact us at <a href='mailto:informaticscafetera@gmail.com' style='color: #2980b9;'>informaticscafetera@gmail.com</a> if this was an error.</p>"
    else:  # "Pending"
        html_message += "<p style='color: #f1c40f;'>Your order status is Pending. We'll keep you posted!</p>"

    html_message += f"""
            <h3 style="margin-top: 20px;">Order Details</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 8px; border: 1px solid #ddd;">Total</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">Rs. {instance.total_price}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">Payment</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{instance.get_payment_method_display()}</td>
                </tr>
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 8px; border: 1px solid #ddd;">Date</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{instance.order_date.strftime('%Y-%m-%d')}</td>
                </tr>
    """
    for index, item in enumerate(instance.order_items.all()):
        bg_color = "#f5f5f5" if index % 2 == 0 else "#ffffff"
        html_message += f"""
                <tr style="background-color: {bg_color};">
                    <td style="padding: 8px; border: 1px solid #ddd;">Food Item {index + 1}</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{item.food_item.name} (x{item.quantity})</td>
                </tr>
        """
    html_message += """
            </table>
            <p style="margin-top: 20px;">Thank you,<br><strong>Informatics Cafeteria</strong></p>
            <footer style="font-size: 12px; color: #777; margin-top: 20px; text-align: center;">
                Informatics Cafeteria | <a href="mailto:informaticscafetera@gmail.com" style="color: #2980b9;">Contact Us</a>
            </footer>
        </div>
    </body>
    </html>
    """
    return subject, plain_message, html_message

# Signal for order updates
@receiver(pre_save, sender=Order)
def send_order_status_update_email(sender, instance, **kwargs):
    if instance.pk:  # Only trigger on updates
        try:
            old_order = Order.objects.get(pk=instance.pk)
            if old_order.status != instance.status:  # Status changed
                subject, plain_message, html_message = build_email_content(instance, is_creation=False)
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
        except Order.DoesNotExist:
            pass

# Signal for order creation
@receiver(post_save, sender=Order)
def send_order_creation_email(sender, instance, created, **kwargs):
    if created and instance.status == "Pending":  # Only trigger on creation with "Pending"
        subject, plain_message, html_message = build_email_content(instance, is_creation=True)
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            html_message=html_message,
            fail_silently=False,
        )