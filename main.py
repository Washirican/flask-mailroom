import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all_donations'))


@app.route('/donations/')
def all_donations():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/donors/')
def all_donors():
    donors = Donor.select()
    return render_template('donors.jinja2', donors=donors)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Checks if form is blank and displays message
        if request.form['donor'] == '' or request.form['donation'] == '':
            return render_template(
                'create.jinja2',
                error='Please, provide donor name and donation amount!'
                )

        else:
            try:
                donor_id = Donor.get(Donor.name == request.form['donor']).id
            except Donor.DoesNotExist:
                return render_template(
                    'create.jinja2',
                    error='Donor name could not be found!'
                    )
            donation = request.form['donation']

            new_donation = Donation(value=donation, donor=donor_id)
            new_donation.save()

            return redirect(url_for('all_donations'))
    else:
        return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

