# `support@carrierpress.com` bounces. Fixing it.

Written 2026-09-13. **The change itself needs the GoDaddy login, so it is
Jeffrey's.** Everything that can be worked out beforehand is below.

## What is actually wrong

`carrierpress.com` has **no MX records at all**, so there is nowhere for mail to
that domain to be delivered. Every message to `support@carrierpress.com` bounces.

That address appears in **36 files** in this repo — including `make_privacy.py`
and **every app privacy policy** — and on the Home Rule support page. Apple reads
the privacy and support URLs during App Review, so this is on the launch path.

Outbound is fine and unaffected: the MailerLite newsletter sends through
`_spf.mlsend.com` with DKIM at `litesrv._domainkey`. **This is purely about
receiving.**

## 🔴 Read this before adding any MX record

The SPF chain today is:

```
carrierpress.com            TXT   v=spf1 include:dc-db9e4b7a04._spfm.carrierpress.com ~all
dc-db9e4b7a04._spfm         TXT   v=spf1 a mx include:_spf.mlsend.com ~all
```

⚠️ **That nested record contains the `mx` mechanism.** `mx` means *"any host
listed in this domain's MX records is authorised to send as this domain."*

Right now it authorises **nothing**, because there are no MX records. **The
moment an MX record is added, whatever it points at silently becomes an
authorised sender for `carrierpress.com`** — and for a shared forwarding
service that is a lot of infrastructure, handling mail for many other domains.

▶ **Nothing needs `mx` to be there.** MailerLite sends via the `include:`, and
`a` covers the apex, which is GitHub Pages and sends no mail. Removing `mx` from
that nested record would be the tighter configuration.
⛔ **But it is marked PROTECTED in `DNS_BASELINE_2026-08-28.txt` and it is a
GoDaddy-generated SPF-merge record** (`_spfm`), so do not edit it casually. This
is a flag, not an instruction: add the MX first, confirm mail flows, and treat
the SPF tightening as a separate, reversible change.

## The fix

⭐ **Keep DNS at GoDaddy.** `DEPLOY.md` already settled this: moving nameservers
to Cloudflare means recreating all 12 records including the protected DKIM and
SPF, which is *"more chances to break email."* Adding two MX records at GoDaddy
touches nothing that exists.

### Option A — GoDaddy's own forwarding, if it is included

Check **GoDaddy → carrierpress.com → Email → Forwarding** first. If the domain
includes it, this is the fewest moving parts and no new vendor. GoDaddy sets the
MX records itself. ⚠️ GoDaddy pushes a Microsoft 365 trial on this screen; the
forwarding option is the free one, if it is offered at all.

### Option B — a free forwarder, which is what to use if A costs money

Add these two records in **GoDaddy → DNS → Records**, changing nothing else:

| Type | Name | Value | Priority | TTL |
|---|---|---|---|---|
| MX | `@` | `mx1.improvmx.com` | 10 | 1 hour |
| MX | `@` | `mx2.improvmx.com` | 20 | 1 hour |

Both hosts verified to resolve 2026-09-13. Then create the free account at
improvmx.com, add `carrierpress.com`, and forward `support@` to
`carrier.jeffrey@gmail.com`.

⚠️ **Free forwarding RECEIVES; it does not SEND.** Replies will come from the
Gmail address unless Gmail's *Send mail as* is set up afterwards, which needs an
SMTP credential and an SPF entry. **Receiving is what unblocks the App Store —
do that first and decide about sending later.**

## Verifying it worked

```bash
dig +short MX carrierpress.com          # expect the two hosts, 10 and 20
```

Then actually send a message to `support@carrierpress.com` from an address that
is not the forwarding destination, and confirm it arrives. **A resolving MX
record is not proof of delivery** — the same distinction as an `eas submit` that
exits 0 without Apple having accepted the build.

## Afterwards

- ✅ 36 files stop pointing at a dead mailbox, including every app privacy policy
- ✅ The Home Rule support page has a contact route that works
- ⏭ Consider whether `mx` should stay in the SPF chain, as a separate change
