from flask_login import login_required , current_user
from flask import redirect , url_for , abort
from functools import wraps


def admin_required(f):
  @wraps(f)
  @login_required
  def decorated_function(*args, **kwargs):
    
    if not current_user.is_admin:
      abort(403)
    return f(*args, **kwargs)
  return decorated_function
