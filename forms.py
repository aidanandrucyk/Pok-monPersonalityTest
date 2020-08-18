from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    username = StringField('Name (Optional)')
    email = StringField('Email (Optional)')
    q1 = SelectField('You feel lonely in a large crowd of people', [DataRequired()],
                        choices=[('I20', 'Strongly Agree'),
                                 ('I10', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('E10', 'Disagree'),
                                 ('E20', 'Strongly Disagree')])
    q2 = SelectField('You often consider impractical yet intriguing ideas', [DataRequired()],
                        choices=[('N20', 'Strongly Agree'),
                                 ('N10', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('S10', 'Disagree'),
                                 ('S20', 'Strongly Disagree')])
    q3 = SelectField('You find it challenging to empathize with others', [DataRequired()],
                        choices=[('T20', 'Strongly Agree'),
                                 ('T10', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('F10', 'Disagree'),
                                 ('F20', 'Strongly Disagree')])
    q4 = SelectField('You plan and stick to your travel iternary', [DataRequired()],
                        choices=[('J20', 'Strongly Agree'),
                                 ('J10', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('P10', 'Disagree'),
                                 ('P20', 'Strongly Disagree')])
    submit = SubmitField('Submit')