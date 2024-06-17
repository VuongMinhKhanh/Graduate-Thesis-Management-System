from django.core.mail import send_mail
from django.conf import settings


def send_mail_for_thesis(data):
    username = data["mssv"]["username"]
    subject = f"Notification of Thesis Evaluation Result - {username}"
    thesis_name = data["ten_khoa_luan"]
    score = data["diem_tong"]
    plagiarism = data["ty_le_dao_van"]
    email = data["mssv"]["email"]

    message = (f"Title of Thesis: {thesis_name}\n"
               f"Percentage of plagiarism: {plagiarism}%\n"
               f"Total Score: {score}/10")
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email, ]
    )

# Subject: Notification of Thesis Evaluation Result - [Student's Full Name]
#
# Dear [Student's Full Name],
#
# I hope this message finds you well. We are writing to inform you of the evaluation results for your graduate thesis titled "[Thesis Title]" which you submitted as part of the requirements for your [Degree Program, e.g., Master's or PhD] at [University/College Name].
#
# After a thorough review by the designated committee, we are pleased to present the details of your assessment:
#
# Title of Thesis: [Thesis Title]
# Student ID: [Student ID]
# Total Score: [Total Score]/[Maximum Score Possible]
# Percentage: [Percentage]%
# Grade: [Assigned Grade, if applicable]
# [Optional: Include a brief comment about the thesis quality, strengths, or areas for improvement.]
#
# We would like to congratulate you on the hard work and dedication you have demonstrated throughout your research and writing process. The score reflects the quality and integrity of your scholarly work.
#
# Please note that official documentation regarding your thesis evaluation and any subsequent graduation procedures will be provided by the [University's Office of Academic Affairs/Graduate Studies Office].
#
# Should you have any questions or require further clarification, do not hesitate to contact us at [Contact Information] or during office hours.
#
# Once again, congratulations on reaching this significant milestone in your academic journey. We wish you the best in your future endeavors.
#
# Warm regards,
#
# [Your Full Name]
# [Your Position/Title]
# [Department Name]
# [University/College Name]
# [Contact Information]