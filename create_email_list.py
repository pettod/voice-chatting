import os


def create_email_list():
    try:
        emails_data = []
        # Check if emails file exists
        if os.path.exists('emails/emails.txt'):
            with open('emails/emails.txt', 'r') as f:
                lines = f.readlines()
                for index, line in enumerate(lines, 1):
                    line = line.strip()
                    if line:
                        # Split the line into timestamp and email
                        parts = line.split(' - ', 1)
                        if len(parts) == 2:
                            timestamp, email = parts
                            emails_data.append((index, timestamp, email))
        
        # Read the template file
        with open('email_list.html', 'r') as template_file:
            template_content = template_file.read()
        
        # Simple template rendering
        if emails_data:
            rows_html = ""
            for index, timestamp, email in emails_data:
                rows_html += f"""
                    <tr>
                        <td>{index}</td>
                        <td>{timestamp}</td>
                        <td>{email}</td>
                    </tr>
                """
            template_content = template_content.replace("{% if emails %}", "")
            template_content = template_content.replace("{% for index, timestamp, email in emails %}", "")
            template_content = template_content.replace("{% endfor %}", "")
            template_content = template_content.replace("{% else %}", "")
            template_content = template_content.replace("{% endif %}", "")
            template_content = template_content.replace('<tr>\n                        <td>{{ index }}</td>\n                        <td>{{ timestamp }}</td>\n                        <td>{{ email }}</td>\n                    </tr>', rows_html)
        else:
            # No emails found
            template_content = template_content.replace("{% if emails %}", "")
            template_content = template_content.replace("{% for index, timestamp, email in emails %}", "")
            template_content = template_content.replace("{% endfor %}", "")
            template_content = template_content.replace("{% else %}", "")
            template_content = template_content.replace("{% endif %}", "")
            template_content = template_content.replace('<tr>\n                        <td>{{ index }}</td>\n                        <td>{{ timestamp }}</td>\n                        <td>{{ email }}</td>\n                    </tr>', "")
            template_content = template_content.replace('<tr>\n                    <td colspan="3" class="no-emails">No email subscriptions found.</td>\n                </tr>', '<tr>\n                    <td colspan="3" class="no-emails">No email subscriptions found.</td>\n                </tr>')
        
        return template_content
    except Exception as e:
        return f"<h1>Error loading email list</h1><p>{str(e)}</p>"
