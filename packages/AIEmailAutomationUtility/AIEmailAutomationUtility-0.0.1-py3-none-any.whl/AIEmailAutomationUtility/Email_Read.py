import imaplib
import email
import loggerutility as logger 



class Email_Read:
    def read_email(self, email_config):
        """
        Reads emails from the inbox and returns relevant details
        
        Args:
            email_config (dict): Contains email configuration details
                - host: IMAP host server
                - port: IMAP port
                - email: Email address
                - password: Email password
                
        Returns:
            list: List of dictionaries containing email details
        """
        try:
            mail = imaplib.IMAP4_SSL(email_config['host'], email_config['port'])
            mail.login(email_config['email'], email_config['password'])
            logger.log("login successfully")
            mail.select('inbox')

            
            status, email_ids = mail.search(None, 'UNSEEN')
            emails = []
            
            if status == 'OK':
                email_ids = email_ids[0].split()
                
                for email_id in email_ids:
                    email_body = ""
                    status, data = mail.fetch(email_id, '(RFC822)')
                    
                    if status == 'OK':
                        raw_email = data[0][1]
                        msg = email.message_from_bytes(raw_email)
                        
                        sender_email = msg['From']
                        cc_email = msg['CC']
                        bcc_email = msg['BCC']
                        subject = msg['Subject']
                        
                        # Extract email body
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    email_body += part.get_payload(decode=True).decode()
                        else:
                            email_body = msg.get_payload(decode=True).decode()
                            
                        emails.append({
                            'id': email_id,
                            'sender': sender_email,
                            'cc': cc_email,
                            'bcc': bcc_email,
                            'subject': subject,
                            'body': email_body
                        })
                # logger.log(f"emails:: {emails}")
            return emails
            
        except Exception as e:
            logger.log(f"Error reading emails: {str(e)}")
            raise
        finally:
            try:
                mail.close()
                mail.logout()
            except:
                pass
