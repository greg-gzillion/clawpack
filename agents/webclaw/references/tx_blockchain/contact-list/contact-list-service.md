# Contact List Service

The Contact List Service provides RESTful interfaces for managing marketing contacts and email subscriptions. It allows upserting (insert or update) email addresses into a contact list for marketing communications.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Contact List Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoint │ │
│ │ │ │
│ │ POST /marketing/email/upsert │ │
│ │ (Upsert email into contact list) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────────┬───────────────────┬─────────────────────────────┤ │
│ │ Contact List Store│ User Store │ Role Store │ │
│ │ │ │ │ │
│ │ Organization Store│ Auth Firebase │ Feature Flag Store │ │
│ │ │ Service │ │ │
│ └───────────────────┴───────────────────┴─────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Data Storage │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Contact List Database (Email, Name, Company, URL, Timestamps) │ │
│ │ • Audit Trail │ │
│ │ • Subscription Preferences │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| POST /api/marketing/email/upsert | None (Public) | Upsert email into contact list |

**Note:** This endpoint is intentionally public to allow users to subscribe to marketing communications without authentication. All other services use standard authentication.

## Data Models

### Contact Request Object

| Field | Type | Description | Required | Max Length |
|-------|------|-------------|----------|------------|
| Email | string | Valid email address | Yes | 255 |
| Name | string | Contact's full name | No | 255 |
| CompanyName | string | Contact's company name | No | 255 |
| URL | string | Contact's website URL | No | 500 |

### Contact Database Record

| Field | Type | Description |
|-------|------|-------------|
| Email | string | Primary key - email address |
| Name | string | Contact's name |
| CompanyName | string | Company name |
| URL | Website URL |
| CreatedAt | Timestamp | When record was created |
| UpdatedAt | Timestamp | When record was last updated |
| Status | int | Subscription status (1=Active, 2=Unsubscribed) |
| Source | string | How contact was acquired (e.g., "website_form", "api") |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

## API Endpoints

### POST /api/marketing/email/upsert

Upserts (inserts or updates) an email address into the contact list. If the email already exists, the record is updated with the new information. This endpoint is intentionally public to allow users to subscribe without authentication.

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |

**Note:** Unlike most other services, this endpoint does NOT require:
- Authentication (no Authorization header)
- Network header
- OrganizationID header

This allows users to subscribe to marketing communications without having an account.

#### Request Body

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| Email | string | Valid email address | Yes |
| Name | string | Contact's full name | No |
| CompanyName | string | Contact's company name | No |
| URL | string | Contact's website URL | No |

#### Email Validation

The service validates email addresses with the following rules:

| Rule | Description |
|------|-------------|
| Format | Must be valid email format (local@domain) |
| Length | Max 255 characters |
| Characters | Allowed: letters, numbers, dots, hyphens, underscores, plus signs |
| Domain | Must have valid domain with TLD |

#### Example Request

```bash
curl -X POST \
  "https://api.sologenic.com/api/marketing/email/upsert" \
  -H "Content-Type: application/json" \
  -d '{
    "Email": "john.doe@example.com",
    "Name": "John Doe",
    "CompanyName": "Acme Corporation",
    "URL": "https://acme.com"
  }'
Minimal Request (Email Only)
bash
curl -X POST \
  "https://api.sologenic.com/api/marketing/email/upsert" \
  -H "Content-Type: application/json" \
  -d '{
    "Email": "user@example.com"
  }'
Response
Always returns 200 OK (even for errors, to prevent email enumeration attacks)

json
{
  "message": "Email upserted successfully"
}
Error Response (Still 200 OK for security)
Even when validation fails, the endpoint returns 200 OK to prevent email enumeration attacks. The response body indicates success, but the record is not actually stored.

json
{
  "message": "Email upserted successfully"
}
Security Note: The endpoint always returns 200 OK regardless of whether the email was actually upserted. This prevents attackers from determining which emails exist in the system.

Upsert Behavior
Insert (New Email)
When an email does not exist in the contact list:

text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Insert Behavior                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Request: POST /marketing/email/upsert                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ {                                                                     │   │
│  │   "Email": "new@example.com",                                         │   │
│  │   "Name": "New User",                                                 │   │
│  │   "CompanyName": "New Company",                                       │   │
│  │   "URL": "https://newcompany.com"                                     │   │
│  │ }                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Database Action: INSERT                                              │   │
│  │                                                                      │   │
│  │ • New record created                                                 │   │
│  │ • CreatedAt = now()                                                  │   │
│  │ • UpdatedAt = now()                                                  │   │
│  │ • Status = ACTIVE (1)                                                │   │
│  │ • Source = "api"                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Response: 200 OK                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Update (Existing Email)
When an email already exists in the contact list:

text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Update Behavior                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Request: POST /marketing/email/upsert                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ {                                                                     │   │
│  │   "Email": "existing@example.com",                                    │   │
│  │   "Name": "Updated Name",  ← Changed                                  │   │
│  │   "CompanyName": "Updated Company",  ← Changed                        │   │
│  │   "URL": "https://updated.com"  ← Changed                             │   │
│  │ }                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Database Action: UPDATE                                              │   │
│  │                                                                      │   │
│  │ • Existing record updated                                            │   │
│  │ • CreatedAt unchanged                                                │   │
│  │ • UpdatedAt = now()                                                  │   │
│  │ • Only provided fields are updated                                   │   │
│  │ • Missing fields retain previous values                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Response: 200 OK                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Partial Update Example
If you only provide the Email field, existing data is preserved:

bash
# First request - creates full record
curl -X POST /api/marketing/email/upsert \
  -d '{
    "Email": "user@example.com",
    "Name": "Original Name",
    "CompanyName": "Original Company"
  }'

# Second request - only updates Name, preserves CompanyName
curl -X POST /api/marketing/email/upsert \
  -d '{
    "Email": "user@example.com",
    "Name": "New Name"
  }'

# Result: Name="New Name", CompanyName="Original Company"
Use Cases
Newsletter Subscription
bash
curl -X POST "https://api.sologenic.com/api/marketing/email/upsert" \
  -H "Content-Type: application/json" \
  -d '{
    "Email": "subscriber@example.com",
    "Name": "Newsletter Subscriber"
  }'
Business Contact Collection
bash
curl -X POST "https://api.sologenic.com/api/marketing/email/upsert" \
  -H "Content-Type: application/json" \
  -d '{
    "Email": "contact@company.com",
    "Name": "Jane Smith",
    "CompanyName": "Tech Innovations Inc.",
    "URL": "https://techinnovations.com"
  }'
Event Registration
bash
curl -X POST "https://api.sologenic.com/api/marketing/email/upsert" \
  -H "Content-Type: application/json" \
  -d '{
    "Email": "attendee@example.com",
    "Name": "Event Attendee",
    "CompanyName": "Attendee Company"
  }'
Whitepaper Download
bash
# After user downloads a whitepaper, capture their contact info
curl -X POST "https://api.sologenic.com/api/marketing/email/upsert" \
  -H "Content-Type: application/json" \
  -d '{
    "Email": "reader@example.com",
    "Name": "John Reader",
    "CompanyName": "Research Corp"
  }'
Integration Examples
Web Form Integration (HTML/JavaScript)
html
<!-- Contact Form -->
<form id="contactForm">
  <input type="email" id="email" placeholder="Email" required>
  <input type="text" id="name" placeholder="Full Name">
  <input type="text" id="company" placeholder="Company Name">
  <input type="url" id="url" placeholder="Website URL">
  <button type="submit">Subscribe</button>
</form>

<script>
document.getElementById('contactForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const data = {
    Email: document.getElementById('email').value,
    Name: document.getElementById('name').value,
    CompanyName: document.getElementById('company').value,
    URL: document.getElementById('url').value
  };
  
  const response = await fetch('https://api.sologenic.com/api/marketing/email/upsert', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  
  if (response.ok) {
    alert('Thank you for subscribing!');
    document.getElementById('contactForm').reset();
  }
});
</script>
React Component Example
jsx
import React, { useState } from 'react';

function NewsletterSignup() {
  const [formData, setFormData] = useState({
    email: '',
    name: '',
    companyName: '',
    url: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('https://api.sologenic.com/api/marketing/email/upsert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          Email: formData.email,
          Name: formData.name,
          CompanyName: formData.companyName,
          URL: formData.url
        })
      });
      
      if (response.ok) {
        setSubmitted(true);
        setFormData({ email: '', name: '', companyName: '', url: '' });
      }
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (submitted) {
    return (
      <div className="success-message">
        <h3>Thank You!</h3>
        <p>You've been added to our mailing list.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="newsletter-form">
      <h2>Subscribe to our newsletter</h2>
      
      <input
        type="email"
        name="email"
        placeholder="Email Address *"
        value={formData.email}
        onChange={handleChange}
        required
      />
      
      <input
        type="text"
        name="name"
        placeholder="Full Name"
        value={formData.name}
        onChange={handleChange}
      />
      
      <input
        type="text"
        name="companyName"
        placeholder="Company Name"
        value={formData.companyName}
        onChange={handleChange}
      />
      
      <input
        type="url"
        name="url"
        placeholder="Website URL"
        value={formData.url}
        onChange={handleChange}
      />
      
      <button type="submit">Subscribe</button>
    </form>
  );
}

export default NewsletterSignup;
Node.js Backend Integration
javascript
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

// Endpoint to handle contact form submissions
app.post('/api/contact', async (req, res) => {
  const { email, name, company, website } = req.body;
  
  try {
    // Forward to Contact List Service
    await axios.post('https://api.sologenic.com/api/marketing/email/upsert', {
      Email: email,
      Name: name,
      CompanyName: company,
      URL: website
    }, {
      headers: { 'Content-Type': 'application/json' }
    });
    
    res.json({ success: true, message: 'Contact added successfully' });
  } catch (error) {
    console.error('Error adding to contact list:', error.message);
    // Still return success to user to prevent enumeration
    res.json({ success: true, message: 'Contact added successfully' });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
Python Integration
python
import requests
from typing import Optional

class ContactListService:
    """Client for Contact List Service"""
    
    BASE_URL = "https://api.sologenic.com/api/marketing/email/upsert"
    
    @classmethod
    def upsert_contact(cls, 
                       email: str, 
                       name: Optional[str] = None,
                       company_name: Optional[str] = None,
                       url: Optional[str] = None) -> bool:
        """
        Upsert a contact into the marketing list.
        
        Args:
            email: Contact's email address (required)
            name: Contact's full name (optional)
            company_name: Contact's company name (optional)
            url: Contact's website URL (optional)
        
        Returns:
            bool: Always returns True (API always returns 200)
        """
        payload = {"Email": email}
        
        if name:
            payload["Name"] = name
        if company_name:
            payload["CompanyName"] = company_name
        if url:
            payload["URL"] = url
        
        try:
            response = requests.post(
                cls.BASE_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response.status_code == 200
        except requests.RequestException:
            # Always return True to prevent enumeration
            return True
    
    @classmethod
    def add_newsletter_subscriber(cls, email: str, name: Optional[str] = None):
        """Add a newsletter subscriber"""
        return cls.upsert_contact(email=email, name=name)
    
    @classmethod
    def add_business_lead(cls, email: str, company_name: str, name: Optional[str] = None):
        """Add a business lead"""
        return cls.upsert_contact(
            email=email,
            name=name,
            company_name=company_name
        )

# Usage examples
ContactListService.add_newsletter_subscriber("user@example.com", "John Doe")
ContactListService.add_business_lead("lead@company.com", "Tech Corp", "Jane Smith")
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/http/
CONTACT_LIST_STORE	Contact list service endpoint	github.com/sologenic/com-fs-contact-list-model
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
USER_STORE	User management service	github.com/sologenic/com-fs-user-model
ROLE_STORE	Role management service	github.com/sologenic/com-fs-role-model
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-model
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-feature-flag-model
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
RATE_LIMIT_REQUESTS	Rate limit requests per minute	60
RATE_LIMIT_WINDOW	Rate limit window in seconds	60
ALLOW_DUPLICATE_EMAILS	Allow duplicate email entries	false
Example Environment Configuration
bash
# Required
CONTACT_LIST_STORE=localhost:50061
AUTH_FIREBASE_SERVICE=localhost:50070
USER_STORE=localhost:50049
ROLE_STORE=localhost:50066
ORGANIZATION_STORE=localhost:50060
FEATURE_FLAG_STORE=localhost:50055

# Optional
LOG_LEVEL=info
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW=60
ALLOW_DUPLICATE_EMAILS=false

# HTTP Configuration
HTTP_CONFIG='{
  "port": ":8080",
  "cors": {
    "allowedOrigins": ["*"]
  },
  "timeouts": {
    "read": "10s",
    "write": "10s",
    "idle": "10s",
    "shutdown": "10s"
  }
}'
Docker Compose Example
yaml
version: '3.8'

services:
  contact-list-service:
    image: sologenic/contact-list-service:latest
    environment:
      - CONTACT_LIST_STORE=contact-list-store:50061
      - AUTH_FIREBASE_SERVICE=auth-service:50070
      - USER_STORE=user-service:50049
      - ROLE_STORE=role-service:50066
      - ORGANIZATION_STORE=organization-service:50060
      - FEATURE_FLAG_STORE=feature-flag-service:50055
      - LOG_LEVEL=info
      - RATE_LIMIT_REQUESTS=60
    ports:
      - "8080:8080"
    networks:
      - internal

  contact-list-store:
    image: sologenic/contact-list-store:latest
    environment:
      - DATABASE_URL=postgres://user:pass@postgres:5432/contacts
    networks:
      - internal

networks:
  internal:
    driver: bridge
Security Considerations
Email Enumeration Prevention
The endpoint always returns 200 OK regardless of success or failure. This prevents:

Attackers from determining which emails exist in the system

Harvesting of valid email addresses

User enumeration attacks

Rate Limiting
Implement rate limiting to prevent abuse:

yaml
# Rate limiting configuration
RATE_LIMIT_REQUESTS=30    # Maximum requests per window
RATE_LIMIT_WINDOW=60      # Window in seconds
Input Validation
All inputs should be validated on the backend:

Field	Validation Rules
Email	Valid format, max 255 chars, no SQL injection
Name	Max 255 chars, sanitized
CompanyName	Max 255 chars, sanitized
URL	Valid URL format, max 500 chars, HTTPS recommended
GDPR Compliance
When collecting contact information for marketing purposes, ensure compliance with GDPR and other privacy regulations:

Required Disclosures
html
<form>
  <input type="email" placeholder="Email" required>
  
  <label>
    <input type="checkbox" required>
    I agree to receive marketing communications and accept the 
    <a href="/privacy">Privacy Policy</a> and 
    <a href="/terms">Terms of Service</a>.
  </label>
  
  <button type="submit">Subscribe</button>
</form>
Data Processing Records
The service automatically tracks:

Creation timestamp (CreatedAt)

Update timestamp (UpdatedAt)

Source of acquisition (implied from endpoint usage)

User Rights Support
To support GDPR rights (right to be forgotten, data access, etc.):

javascript
// Request data deletion
async function requestDeletion(email) {
  // This would be a separate admin endpoint
  const response = await fetch('/api/admin/contact-list/delete', {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer <admin-token>'
    },
    body: JSON.stringify({ Email: email })
  });
  
  return response.ok;
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Email not added	Invalid email format	Validate email before sending
Duplicate entries	ALLOW_DUPLICATE_EMAILS=false	Use upsert instead of insert
Rate limit exceeded	Too many requests	Implement exponential backoff
CORS errors	Missing CORS headers	Configure allowedOrigins in HTTP_CONFIG
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Test the endpoint manually:

bash
# Test with valid email
curl -X POST "https://api.sologenic.com/api/marketing/email/upsert" \
  -H "Content-Type: application/json" \
  -d '{"Email": "test@example.com", "Name": "Test User"}' \
  -v

# Test with invalid email (still returns 200)
curl -X POST "https://api.sologenic.com/api/marketing/email/upsert" \
  -H "Content-Type: application/json" \
  -d '{"Email": "invalid-email", "Name": "Test"}' \
  -v
Check service health:

bash
curl -X GET "https://api.sologenic.com/health" \
  -H "Content-Type: application/json"
Best Practices
Form Design
Double Opt-in: Send confirmation email before adding to active marketing list

Clear Privacy Policy: Link to privacy policy near the submit button

CAPTCHA: Implement CAPTCHA for public forms to prevent bot submissions

Progress Indicators: Show loading state while submitting

Data Management
Regular Cleaning: Remove invalid emails and hard bounces

Unsubscribe Handling: Process unsubscribe requests promptly

Data Minimization: Only collect necessary fields

Audit Trail: Log all upsert operations for compliance

Performance
Scenario	Recommendation
High traffic	Implement request queuing
Bulk imports	Use batch endpoint if available
Real-time validation	Validate email format client-side first
Security
HTTPS Only: Always use HTTPS in production

Input Sanitization: Sanitize all inputs to prevent injection

Rate Limiting: Implement per-IP rate limiting

Logging: Log all requests for audit purposes (without sensitive data)

Related Services
Service	Description
Admin Contact Service	Admin operations (export, delete, manage)
Notification Service	Email sending and marketing campaigns
User Service	User account management
Organization Service	Tenant isolation
License
This documentation is part of the TX Marketplace platform.
