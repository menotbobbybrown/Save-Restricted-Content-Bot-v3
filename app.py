# Copyright (c) 2025 Contributor : https://github.com/Contributor.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os
from flask import Flask, render_template
from config import BOT_NAME, JOIN_LINK, OWNER_USERNAME

app = Flask(__name__)

@app.route("/")
def welcome():
    # Render the welcome page with bot name and links
    return render_template("welcome.html", bot_name=BOT_NAME, join_link=JOIN_LINK, owner_username=OWNER_USERNAME)

if __name__ == "__main__":
    # Default to port 5000 if PORT is not set in the environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
