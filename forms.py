from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    username = StringField('Name (Optional)')
    email = StringField('Email (Optional)')
    q1 = SelectField('You feel lonely in a large crowd of people', [DataRequired()],
                        choices=[('I30', 'Strongly Agree'),
                                 ('I15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('E15', 'Disagree'),
                                 ('E30', 'Strongly Disagree')])
    q2 = SelectField('You often consider impractical yet intriguing ideas', [DataRequired()],
                        choices=[('N30', 'Strongly Agree'),
                                 ('N15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('S15', 'Disagree'),
                                 ('S30', 'Strongly Disagree')])
    q3 = SelectField('You find it challenging to empathize with others', [DataRequired()],
                        choices=[('T30', 'Strongly Agree'),
                                 ('T15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('F15', 'Disagree'),
                                 ('F30', 'Strongly Disagree')])
    q4 = SelectField('You plan and stick to your travel iternary', [DataRequired()],
                        choices=[('J30', 'Strongly Agree'),
                                 ('J15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('P15', 'Disagree'),
                                 ('P30', 'Strongly Disagree')])
    q5 = SelectField('You tend to think out loud', [DataRequired()],
                        choices=[('E30', 'Strongly Agree'),
                                 ('E15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('I15', 'Disagree'),
                                 ('I30', 'Strongly Disagree')])
    q6 = SelectField('You imagine the world as it is rather than how it could be', [DataRequired()],
                        choices=[('S30', 'Strongly Agree'),
                                 ('S15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('N15', 'Disagree'),
                                 ('N30', 'Strongly Disagree')])
    q7 = SelectField('You enjoy finding flaws in an argument', [DataRequired()],
                        choices=[('T30', 'Strongly Agree'),
                                 ('T15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('F15', 'Disagree'),
                                 ('F30', 'Strongly Disagree')])
    q8 = SelectField('You prefer to leave your options open', [DataRequired()],
                        choices=[('P30', 'Strongly Agree'),
                                 ('P15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('J15', 'Disagree'),
                                 ('J30', 'Strongly Disagree')])
    q9 = SelectField('You feel lonely in a large crowd of people', [DataRequired()],
                        choices=[('I30', 'Strongly Agree'),
                                 ('I15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('E15', 'Disagree'),
                                 ('E30', 'Strongly Disagree')])
    q10 = SelectField('You attention to concrete facts and details', [DataRequired()],
                        choices=[('S30', 'Strongly Agree'),
                                 ('S15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('N15', 'Disagree'),
                                 ('N30', 'Strongly Disagree')])
    q11 = SelectField('You often consider others when making decisions', [DataRequired()],
                        choices=[('F30', 'Strongly Agree'),
                                 ('F15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('T15', 'Disagree'),
                                 ('T30', 'Strongly Disagree')])
    q12 = SelectField('You often see deadlines and rules as flexible', [DataRequired()],
                        choices=[('P30', 'Strongly Agree'),
                                 ('P15', 'Agree'),
                                 ('0', 'Neutral'),
                                 ('J15', 'Disagree'),
                                 ('J30', 'Strongly Disagree')])
    submit = SubmitField('Submit')