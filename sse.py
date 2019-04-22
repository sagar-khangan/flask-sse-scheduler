from flask import Flask, render_template
from flask_sse import sse
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


def sensor():
    """ Function for test purposes. """
    with app.app_context():
        sse.publish({"message": datetime.datetime.now()}, type='greeting')
        print("Scheduler is alive!")


sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=10)
sched.start()


@app.route('/')
def index():
    return render_template("/index.html")


if __name__ == '__main__':
   app.run(debug=True)