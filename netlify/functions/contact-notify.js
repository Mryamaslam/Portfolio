const EMAILJS = {
  serviceId: process.env.EMAILJS_SERVICE_ID || 'service_2ph8u3w',
  templateId: process.env.EMAILJS_TEMPLATE_ID || 'template_56jyetw',
  publicKey: process.env.EMAILJS_PUBLIC_KEY || 'j3AoH8cf3nfZVbQVN'
};

const NOTIFY_TO = process.env.NOTIFICATION_EMAIL || 'bilalrazaupwork@gmail.com';

exports.handler = async function (event) {
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: corsHeaders(),
      body: ''
    };
  }

  if (event.httpMethod !== 'POST') {
    return json(405, { error: 'Method not allowed' });
  }

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch (_) {
    return json(400, { error: 'Invalid JSON body' });
  }

  const name = String(body.name || '').trim() || 'Website Visitor';
  const email = String(body.email || '').trim().toLowerCase();
  const message = String(body.message || '').trim();

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json(400, { error: 'Valid email is required' });
  }

  try {
    const res = await fetch('https://api.emailjs.com/api/v1.0/email/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        service_id: EMAILJS.serviceId,
        template_id: EMAILJS.templateId,
        user_id: EMAILJS.publicKey,
        template_params: {
          to_email: NOTIFY_TO,
          user_name: name,
          user_email: email,
          from_name: name,
          from_email: email,
          reply_to: email,
          message: message || 'New contact form submission'
        }
      })
    });

    if (!res.ok) {
      const text = await res.text().catch(() => '');
      return json(502, { error: 'EmailJS failed', detail: text || res.status });
    }

    return json(200, { ok: true, sent: true });
  } catch (err) {
    return json(500, { error: err.message || 'Email send failed' });
  }
};

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };
}

function json(statusCode, data) {
  return {
    statusCode,
    headers: { ...corsHeaders(), 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  };
}
