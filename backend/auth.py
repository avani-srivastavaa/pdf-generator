from werkzeug.security import generate_password_hash, check_password_hash

admin_user = "admin"
admin_password = "admin@123"  # <-- set your desired password here
admin_pass_hash = generate_password_hash(admin_password)

def check_login(username, password):
    return username == admin_user and check_password_hash(admin_pass_hash, password)
