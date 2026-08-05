# Lightfunnels API — Knowledge Base

> Comprehensive reference compiled from the official documentation at [developer.lightfunnels.com](https://developer.lightfunnels.com) (fetched 2026-07-22). All 35 documentation pages are included: guides, resource endpoints, and GraphQL type definitions.

## Quick Reference

| Item | Value |
|---|---|
| **API style** | GraphQL (single endpoint, POST) |
| **GraphQL endpoint** | `POST https://services.lightfunnels.com/api/v2` |
| **OAuth consent screen** | `GET https://app.lightfunnels.com/admin/oauth?client_id={id}&redirect_uri={uri}&scope={scopes}&state={state}` |
| **OAuth token exchange** | `POST https://api.lightfunnels.com/oauth/access_token` (JSON body: `client_id`, `client_secret`, `code`) |
| **Auth header** | `Authorization: Bearer <access token>` |
| **Access token lifetime** | Permanent (store it; one token per connected account) |
| **Request params** | `query` (GraphQL string), `variables` (optional JSON object) |
| **Pagination** | Cursor-based (`first`, `after`, `edges/node/cursor`, `pageInfo.endCursor`, `pageInfo.hasNextPage`); default 25, max page size shown in docs is 25 per page default |
| **Errors** | JSON `errors[]` array with `message`, `name`, `key`, `path` |
| **App creation** | [Lightfunnels Partners area](https://partners.lightfunnels.com/) → app → "Configurations" tab for `client ID` / `client secret` |
| **Postman collection** | [Run in Postman](https://god.gw.postman.com/run-collection/16831799-560b18e3-2697-46e4-9ac7-1933d463fb37?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D16831799-560b18e3-2697-46e4-9ac7-1933d463fb37%26entityType%3Dcollection%26workspaceId%3Dfa9c0249-aba8-4d8f-8378-47dad60c4b51) |

### Authorization scopes

`funnels`, `orders`, `products`, `analytics`, `customers`, `discounts`, `contact_form_data`, `settings`

### Webhook events

`app/uninstalled` · `checkout/created` · `checkout/updated` · `contact/signup` · `contact/updated` · `funnel/created` · `funnel/updated` · `funnel/deleted` · `order/created` · `order/confirmed` · `order/updated` · `order/cancelled` · `order/uncancelled` · `order/fulfilled` · `order/refunded` · `payment/created` · `payment/paid` · `product/created` · `product/updated` · `product/deleted`

## Endpoint Index (all operations)

All operations are GraphQL queries/mutations sent to `POST https://services.lightfunnels.com/api/v2`.

| Resource | Operations |
|---|---|
| **Funnels** | List all funnels · Create a funnel · Retrieve a funnel · Update a funnel · Delete a funnel |
| **Stores** | List all stores · Create a store · Retrieve a store · Update a store · Delete a store · Add products to store |
| **Products** | List all products · Create a product · Retrieve a product · Update a product · Delete a product |
| **Bundles** | List all bundles · Create a PriceBundle · Retrieve a bundle · Update a PriceBundle · Delete a PriceBundle |
| **Collections** | List all collections · Create a collection · Retrieve a collection · Update a collection · Delete a collection |
| **Orders** | List all orders · Retrieve an order · Update an order · Cancel an order |
| **Customers** | List all customers · Create a customer · Retrieve a customer · Update a customer |
| **Discounts** | List all discounts · Create a discount · Retrieve a discount · Update a discount · Delete a discount |
| **Segments** | List all segments · Create a segment · Retrieve a segment · Update a segment · Delete a segment |
| **Reviews** | List all reviews · Create a review · Retrieve a review · Update a review · Delete a review |
| **Settings** | Retrieve account pixels · Update account pixels · Create Facebook Conversion API integration · Retrieve integrations · Remove integration |
| **Shipping Rate Groups** | List · Create · Update · Delete |
| **App Charges** | Create app charges · List all app charges · Get an app charge |
| **Webhooks** | List webhooks · Create a webhook · Delete a webhook (see Webhooks guide) |

## Table of Contents

**Part 1 — Guides**
1. Introduction
2. Getting Started
3. Authentication (OAuth2)
4. Embedded Apps
5. Authorization Scopes
6. Errors
7. Webhooks
8. Pagination
9. Charging for Your App

**Part 2 — Resources (Queries & Mutations)**
Funnels · Stores · Products · Bundles · Collections · Orders · Customers · Discounts · Segments · Reviews · Settings · Shipping Rate Groups · App Charges

**Part 3 — GraphQL Types**
Per-resource type definitions plus shared/other types (Money, Image, PageInfo, connections, etc.)

> Note: the official `/settings/types` page returns a 404 on the source site (broken link in their nav); every other page is captured in full below.

---

# Part 1 — Guides

---

## API Documentation

Use the Lightfunnels API to access and manage funnels, products, orders and other resources in order to seamlessly integrate your product into the workflow of thousands of Lightfunnels users.

### Welcome!

To get started, you need to create a Lightfunnels application under the [Lightfunnels Partners area](https://partners.lightfunnels.com/app-charges). Once the application is created, click below to visit our Getting Started page and our Postman collection for step by step instructions. [Getting Started](https://developer.lightfunnels.com/gettingstarted)[![](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/16831799-560b18e3-2697-46e4-9ac7-1933d463fb37?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D16831799-560b18e3-2697-46e4-9ac7-1933d463fb37%26entityType%3Dcollection%26workspaceId%3Dfa9c0249-aba8-4d8f-8378-47dad60c4b51)

### Guides

#### Authentication

Learn how to authenticate your API requests.

[Read more](https://developer.lightfunnels.com/authentication)

#### Charging for your app

Learn how to handle app charges.

[Read more](https://developer.lightfunnels.com/charges)

#### Pagination

Understand how to work with paginated responses.

[Read more](https://developer.lightfunnels.com/pagination)

#### Errors

Read about the different types of errors returned by the API.

[Read more](https://developer.lightfunnels.com/errors)

#### Webhooks

Learn how to programmatically configure webhooks for your app.

[Read more](https://developer.lightfunnels.com/webhooks)

### Resources

#### App charges

Retrieve, create, app charges.

#### Bundles

Retrieve, create, update, and delete bundles.

#### Collections

Retrieve, create, update, and delete collections.

#### Customers

Retrieve, create, update, and delete customers.

#### Discounts

Retrieve, create, update, or delete discounts.

#### Funnels

Retrieve, create, update, or delete funnels.

#### Orders

Retrieve, create, update, or delete orders.

#### Products

Retrieve, create, update, or delete products.

#### Reviews

Retrieve, create, update, or delete reviews.

#### Segments

Retrieve, create, update, or delete segments.

#### Settings

Retrieve, create, update, or delete settings.

#### Stores

Retrieve, create, update, or delete stores.

### Video Tutorials
Welcome to our Video series on using our API to build your First App! In this brief tutorial, we'll cover the fundamental steps to kickstart your app development journey. Whether you're a coding enthusiast or a total beginner, we've got you covered. Let's dive in![![](images/yutab.webp)![](images/thumbnail.jpg)](https://www.lightfunnels.co/academy/apps-development)

---

## Getting Started

Welcome to the Lightfunnels GraphQL API documentation! This page will provide you with an overview of how to get started using the Lightfunnels GraphQL API.

### Prerequisites

Before you start using the Lightfunnels GraphQL API, you will need the following:

- An active Lightfunnels account. You can [sign up for a free trial here](https://app.lightfunnels.com/admin/auth/signup).
- A Lightfunnels Partners account that you can access from [here](https://partners.lightfunnels.com/).
- A Lightfunnels app that you can create inside your Partners account.
- A `client ID` and `client secret`. You can find these under the "Configurations" tab of your app.
- Basic familiarity with [GraphQL](https://graphql.org/).

If you are not familiar with GraphQL, do not worry, you can find a list done for you queries and mutations on our [Postman collection](https://god.gw.postman.com/run-collection/16831799-560b18e3-2697-46e4-9ac7-1933d463fb37?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D16831799-560b18e3-2697-46e4-9ac7-1933d463fb37%26entityType%3Dcollection%26workspaceId%3Dfa9c0249-aba8-4d8f-8378-47dad60c4b51). If you want to learn more about GraphQL, we recommend [this tutorial](https://www.howtographql.com/) to get started.

---

### Making a Query

To make a GraphQL query using the Lightfunnels API, you will need to send an HTTP POST request to the API endpoint with the following parameters:

#### GraphQL API Endpoint

```
https://services.lightfunnels.com/api/v2

```

Parameters:

- `query`: The GraphQL query, encoded as a string
- `variables` (optional): A JSON object containing variables for the query

---

#### Authorization

You should also include your API `access token` in the Authorization header of the request as follows:

#### Authorization header

```
Authorization: Bearer <your access token>

```

Learn how to get your access token on the [Access Token page](https://developer.lightfunnels.com/authentication)

---

### Apps

To access your app, click the "Install app" button on the top right corner of your app page on the [Partners area](https://partners.lightfunnels.com/). This will take you to your Lightfunnels dashboard where your app is located. You can also access your app directly by going to:

```
https://app.lightfunnels.com/admin/apps/{your client id}

```

On this page, your app URL will load inside of an iframe. You can also choose to have your app load outside of the Lightfunnels dashboard by checking the "External" checkbox in your app configuration.

---

### See it live on Postman

Click the button below to open the Lightfunnels collection in Postman and see the API working live.

Make sure you update the variables in the collection settings to your own values.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/16831799-560b18e3-2697-46e4-9ac7-1933d463fb37?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D16831799-560b18e3-2697-46e4-9ac7-1933d463fb37%26entityType%3Dcollection%26workspaceId%3Dfa9c0249-aba8-4d8f-8378-47dad60c4b51)

---

## Authentication

You'll need to authenticate your requests in order to read or write to any private resources on the Lightfunnels API. In this guide, we'll look at how authentication works. Lightfunnels uses the industry-standard protocol for authorization, OAuth2.

### The access token

Think of the access token as a password that lets your app perform actions on an account.

Your app will have a different access token to each account that you want to access. The access token helps identify which account you are trying to access as well as what [actions (see scopes)](https://developer.lightfunnels.com/scopes) you are allowed to take on the account.

### Getting an access token

In order to get the access token for your account, you need to perform the following steps:

1. Send the user to a consent screen to grant permissions to your app
2. Request the access token and save it in order to use it in all your requests

Let's get started

### Step 1 - Consent screen

In order to get an access token, you have to ask the user for the permissions that you want to use.

The way you do that is through a consent screen.

![consent screen](https://developer.lightfunnels.com/screenshots/consent.png)

To create a consent screen you will need the make a GET request in the following format:

#### Consent screen parameters

```
https://app.lightfunnels.com/admin/oauth?client_id={{client_id}}&redirect_uri={{redirect_uri}}&scope={{scopes}}&state={{state}}

```

- `client ID` that you will get after creating your app. Example: `9461026524765762404265764243`
- A comma separated list of [scopes](https://developer.lightfunnels.com/scopes) that you want to get the permission for. Example `products,orders`
- `Redirect URI` where the user will be redirected after they accept the permissions. Example `https://yourapp.com/redirect`
- Optional: `state` parameter that will be returned to you in the redirect URI. Example `123`.

**Important:** The `redirect URI` must be whitelisted in your app configuration.

Using the example values above, this is what your consent screen URL would look like:

#### Example consent screen URL

```
https://app.lightfunnels.com/admin/oauth?client_id=9461026524765762404265764243&redirect_uri=https://yourapp.com/redirect&scope=products,orders&state=123

```

### Step 2 - Getting your access token

Once the user accepts the requested permissions on the consent screen, they will get redirected to the `redirect URI` that you used in Step 1, with an authorization `code` variable added in the query string.

You should send a POST request to `https://api.lightfunnels.com/oauth/access_token` with a JSON body containing your `client_id`, `client_secret`, and the `code` you received. Here is an example ts code:

```
const getOAuthToken = async () => {
  const clientId = 'client_id';
  const clientSecret = 'client_secret';
  const tokenUrl = 'https://api.lightfunnels.com/oauth/access_token';

  try {
    const response = await fetch(tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret,
        code: 'the authorization code from the query string'
      })
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log('OAuth Token Response:', data);
    return data.access_token;
  } catch (error) {
    console.error('OAuth request failed:', error);
    return null;
  }
};

// Call the function
getOAuthToken().then(token => {
  if (token) {
    console.log('Access Token:', token);
  } else {
    console.log('Failed to retrieve access token.');
  }
});

```

#### Response example

```
{
    "access_token": "YOUR_ACCESS_TOKEN",
}

```

### Important notes

- While testing, the authorization code will only work once. If you need to test again, you will need to go through the consent screen again.
- The client secret is private and should never be shared.
- The access token is permanent and should be saved in your database. You will need it for all your requests.

---

## Embedded apps & iframe sessions

When a merchant opens your app from the Lightfunnels admin, your app is loaded inside an `iframe`. This guide explains how to complete OAuth and keep the merchant signed in **inside that iframe** — no popup, no breaking out to a top-level tab, and no sensitive tokens stored in the browser.

If you have not set up OAuth yet, read [Authentication](https://developer.lightfunnels.com/authentication) first. This page builds on it.

### How embedding works

The Lightfunnels admin renders your app inside an iframe and passes a small amount of context on the URL:

#### Embedded app URL

```
https://yourapp.com/?account_id={{account_uid}}&iframe=true

```

- `account_id` — the merchant account the app was opened for.
- `iframe=true` — a hint that your app is running embedded.

These are **hints, not credentials**. They are not signed and must never be trusted on their own to grant access. Authentication still happens through OAuth (below).

Lightfunnels does not currently issue a signed session token per iframe load (there is no "App Bridge"-style primitive). You don't need one — the OAuth flow works inside the iframe, and your app issues its own session. This guide shows how.

### OAuth works inside the iframe

You do **not** need to open a popup or break out to a top-level window to authorize. You can run the entire OAuth flow inside the iframe with a normal, same-frame navigation to the consent screen:

#### Consent screen (navigate the iframe itself)

```
https://app.lightfunnels.com/admin/oauth?client_id={{client_id}}&redirect_uri={{redirect_uri}}&scope={{scopes}}&state={{state}}

```

Trigger it as a same-frame navigation — a server redirect of the iframe's own request, or `window.location.assign(...)` from inside the iframe. **Do not** target `window.top` and **do not** call `window.open`.

#### Start OAuth from inside the iframe

```
// Same-frame navigation — stays in the iframe.
window.location.assign(consentUrl)

// ❌ Do NOT do either of these — they are unnecessary:
// window.top.location.assign(consentUrl)  // breaks out to top-level
// window.open(consentUrl)                 // popup

```

#### Why it works

When your iframe navigates to `app.lightfunnels.com/admin/oauth`, the iframe's document is now on `lightfunnels.com` — the **same site as the top-level admin window** that is hosting it. The merchant's Lightfunnels login cookie is therefore first-party in that context, so the consent screen resolves normally. Third-party-cookie blocking does not apply here, because nothing cross-site is being read.

After the merchant approves, Lightfunnels redirects back to your `redirect_uri` (your origin) with the authorization `code`, still inside the iframe. You then exchange the code for an access token on your server, exactly as described in [Authentication](https://developer.lightfunnels.com/authentication).

### Don't store the access token in the browser

The OAuth access token is a long-lived credential — treat it like a password. Keep it on your **server**, in your database, keyed by account. The browser should never hold it.

This sidesteps the problem developers usually hit: "I can't safely store a token in the browser." Correct — so don't. `localStorage` is readable by any script on the page (XSS), so it is not a safe place for a sensitive token. Keep the access token server-side and give the browser only a **session**, as below.

### Maintaining a session inside the iframe

After OAuth, your app needs to recognise the merchant on subsequent requests. Your app issues and validates this session itself — keep the Lightfunnels access token on your server and hand the browser only a session.

We recommend using a battle-tested auth library rather than rolling your own session logic. [Better Auth](https://www.better-auth.com/) and [NextAuth / Auth.js](https://authjs.dev/) both handle session creation, signing, and cookie management for you. Whichever you choose, configure its session cookie with the attributes below so it works inside the iframe.

#### Session cookie attributes

Set your session cookie with these attributes so it works embedded and stays safe:

#### Set-Cookie

```
Set-Cookie: session=<your-signed-session-id>;
            HttpOnly; Secure; SameSite=None; Partitioned; Path=/

```

- `HttpOnly` — JavaScript can't read it, so XSS can't steal it (the problem `localStorage` has).
- `Secure` — HTTPS only. Required with `SameSite=None`.
- `SameSite=None` — allows the cookie to be sent in the cross-site iframe context.
- `Partitioned` — opts into [CHIPS](https://developers.google.com/privacy-sandbox/cookies/chips). The browser keeps a **separate copy of this cookie per top-level site**, so it can't be used for cross-site tracking — which is why browsers still allow it even with third-party cookies blocked.

The cookie value should be a signed/opaque session id — not the access token. Your server validates the signature, looks up the matching account, and uses the access token (from your database) to call the Lightfunnels API.

`Partitioned` ties the cookie to the Lightfunnels admin (the top-level site). Inside the admin iframe it works. If the same app is also opened in a standalone tab, that is a different partition and won't see this cookie.

### Browser support

- **Chrome / Edge** — full support for `Partitioned` (CHIPS).
- **Firefox / Safari** — partition third-party storage by default, so embedded cookies work; the `Partitioned` attribute may be ignored but the cookie is still isolated. Test your flow in each.
- Most auth libraries don't set `Partitioned` by default — make sure you add it to the session cookie config, or the cookie won't be sent inside the iframe.

### Summary

- Your app runs in an iframe; `account_id` and `iframe=true` are unsigned hints, not auth.
- Run OAuth inside the iframe with a same-frame navigation to `/admin/oauth` — no popup, no `window.top`.
- Keep the access token on your server. Never put it in `localStorage`.
- Issue your own session with a `HttpOnly; Secure; SameSite=None; Partitioned` cookie — ideally via an auth library like Better Auth or NextAuth.

---

## Authorization Scopes

Scopes define what areas of the account your application is permitted to access and take action on.

Scopes are used to generate the consent screen link where the user can accept the permissions you requested. To learn more about this process, refer to the [Authentication](https://developer.lightfunnels.com/authentication) page.

Here is a list of the different scopes that are currently available.

- `funnels` — Allows you to read, create, update and delete funnels and stores.
- `orders` — Allows you to read, create, update and delete orders.
- `products` — Allows you to read, create, update and delete products.
- `analytics` — Allows you to read analytics data.
- `customers` — Allows you to read customers (contacts) data.
- `discounts` — Allows you to read, create, update and delete discounts.
- `contact_form_data` — Allows you to read contact forms data.
- `settings` — Allows you to read and update account settings.

---

## Errors

This document outlines the standard approach for handling errors in our API responses. Our error responses are structured in a JSON format, providing clear and actionable information to the client.

### Error Response Format

Errors are returned in a consistent structure, making it easier for clients to parse and take appropriate actions. Here's the structure of our standard error response:

```
{
    "errors": [
        {
            "message": "You don't have access to this store",
            "name": "ReportedError",
            "key": "errors_store_access",
            "path": []
        }
    ]
}

```

#### Fields Description

- `errors`: An array of error objects.

  - `message`: A human-readable message providing more details about the error.
  - `name`: The name of the error, typically a broad classification like `ReportedError`.
  - `key`: A unique identifier for the error, useful for client-side parsing.
  - `path`: An array that indicates the location of the error, typically used for form validation errors.

### Handling Errors

1. **Parse Error Response**: Always check for the `errors` field in the response.
2. **Identify Error Type**: Use the `key` or `name` to identify the type of error.
3. **User Communication**: Display the `message` to the user if it's intended for them.
4. **Logging and Monitoring**: Log the error details for monitoring and debugging purposes.
5. **Conditional Logic**: Implement conditional logic based on `key` to handle specific errors uniquely.

### Common Error Keys

This section is reserved for providing common error identifiers that you should expect to make sure your business logic is reliable and robust.

#### Products

- `errors_wrong_product` : Meaning that the product cannot be found.
- `errors_dup_slug` : Meaning that the slug of the product that you're attempting to create or update is already existing.

#### Webhooks

- `webhooks_errors_permission` : Means that You don't have access to the requested webhook type.
- `webhooks_duplicated` : Means that the webhook you're attempting to create already exists.
- `webhooks_not_found` : Means that the requested webhook is not found.
- `webhooks_version_error` : Means that you're requesting the creation of a webhook with a deprecated version.

#### Stores

- `errors_duplicated_store_slug` : Means that the store you are using a pre-existing slug when trying to update or create a store.
- `errors_missing_default_collection` : You should always provide a default collection for a store.
- `errors_delete_default_collection` : Deleting a default store collection is prohibited.
- `errors_store_not_found` : The store you are looking for is unfound.

---

## Webhooks

In this guide, we will look at how to register and consume webhooks to integrate your app with Lightfunnels. With webhooks, your app can know when something happens in Lightfunnels, such as when a new order is created.

### Registering webhooks

To register a new webhook, you need to have a URL in your app that Lightfunnels can call. You can configure a new webhook using the following GraphQL mutation:

#### GraphQL Query

```
## Query
mutation CreateWebhookMutation($node: WebhookInput!) {
 createWebhook(node: $node) {
	type
	settings
	url
 }
}

```

```
input WebhookInput {
  type: String!
  url: String!
  version: WebhookVersion
  settings: WebhookSettings!
}

```

```
scalar WebhookSettings = {
	segments_uids?: string[] | undefined;
}

enum WebhookVersion {
  v1
  v2
}

```

#### GraphQL Variables

```
{
    "node": {
        "type": "order/confirmed",
        "url": "https://yourapp.com/webhooks/order-created/{{account-id}}",
        "settings": {}
    }
}

```

The `type` property refers to the event that you would like to listen to. Refer to [event types](https://developer.lightfunnels.com/webhooks#event-types) for a list of available events.

Note that in the above, we pass the `account ID` to the URL so your app knows to which account the webhook call corresponds to. This refers to the ID of the account in your own database.

In this example, we used the `order/confirmed` event. Now, whenever a new order is made, a webhook is fired off and your app receives all the information related to the new order. In the next section, we'll look at how to consume webhooks.

### Consuming webhooks

When your app receives a webhook request from Lightfunnels, you should verify the authenticity of the request by validating the `lightfunnels-hmac` property from the header using your `client secret`.

Here is an exampe code on how to authenticate the request using Note.js.

```
import crypto from "crypto";

// This is an example of a webhook handler implemented in Node.js
const webhookHandler = async (req, res) => {
    try {
        if (!await verifyWebhook(req)) {
            return res.status(403).send("Invalid webhook");
        }

		// Webhook is valid, continue with your logic here

	} catch (error) {
		console.log(error);
		return res.status(500).send("Internal server error");
	}
}

// This function verifies the webhook using the lightfunnels-hmac header
const verifyWebhook = async (req) => {

    // calculate the hmac
    const localyCalculatedHmac = crypto
    .createHmac("sha256", process.env.LF_APP_SECRET)
    .update(JSON.stringify(req.body), "utf8")
    .digest("base64");

    // check if the hmac is the same as the one in the lightfunnels-hmac header
    const hmac = req.headers["lightfunnels-hmac"];
    if(localyCalculatedHmac != hmac){
        // this webhook is fishy, abort!
        return false;
    }

    return true;
}

```

### Deleting webhooks

When your app no longer needs to receive a specefic webhook, you can delete it by its unique ID. This mutation permanently removes the specified webhook from Lightfunnels, preventing any further events from triggering it.

#### GraphQL Mutation

```
mutation webhooksDeleteMutation($id: ID!){
	deleteWebhook(id: $id)
}

```

Variables object will contain only the webhook id, here is an example:

#### GraphQL Variables

```
{
	"id": "webhook_id"
}

```

It will return the deleted webhook ID if the mutation was executed successfully, here is an example:

#### GraphQL Response

```
{
	"data": {
		"deleteWebhook" : "webhook_id"
	}
}

```

---

### Event Types

Here are all the event types.

`order/created`, `order/confirmed`, `order/fulfilled`, `order/cancelled`, `order/uncancelled`, `order/refunded`, `order-item/created`, `order/updated`, `payment/created`, `payment/paid`, `contact-form/created`, `contact/signup`, `contact/updated`, `checkout/created`, `checkout/updated`, `product/updated`, `product/created`, `product/deleted`, `funnel/created`, `funnel/updated`, `funnel/deleted`, `app/uninstalled`

## Order events

- `New order` — *order/created* — This webhook is fired as soon as an order is created. Note that this may not include all items as it's fired before the customer is done purchasing the upsells & downsells.
- `Order confirmation sent` — *order/confirmed* — This webhook is useful for getting all the order information including the upsells and downsells once the customer is done purchasing.
- `Order fulfillment update` — *order/fulfilled* — This webhook is fired when the order fulfillment status is updated.
- `Order cancelled` — *order/cancelled* — This webhook is fired when the order is cancelled.
- `Order uncancelled` — *order/uncancelled* — This webhook is fired when the order is uncancelled.
- `Order refunded` — *order/refunded* — This webhook is fired when the order is refunded.
- `Order item created` — *order-item/created* — This webhook is fired when the order item is created.
- `Order updated` — *order/updated* — This webhook is triggered whenever an update occurs on an order within the platform. It captures a wide range of modifications, including changes to tags, notes, items, refunds, cancellations, or marking an order as paid. Because this webhook is general, it provides notification of updates without specifying the exact nature of the change. To monitor specific order events, consider using the above webhooks.

#### Order created/confirmed payload

```
	{
		"node": {
			"id": "order_qa6C9z7NCHScxJoewz8xK",
			"_id": 2554132,
			"name": "7799",
			"tags": [],
			"test": true,
			"email": "test@lightfunnels.com",
			"items": [
				{
					"id": "vars__DY-kzRSBh_2A3d38kZE7",
					"_id": 3050394,
					"sku": "",
					"image": null,
					"price": 35,
					"title": "Updated Product",
					"carrier": "",
					"options": [],
					"refund_id": null,
					"__typename": "VariantSnapshot",
					"payment_id": "pay_KvHYIzSxNZWnA2XRpHQnF",
					"product_id": "prod_L8WGlMDUfgM6LAivoCZhv",
					"removed_at": null,
					"variant_id": "var_nG3DGrAyPlG2VYqiv2reY",
					"tracking_link": null,
					"custom_options": [],
					"customer_files": [],
					"tracking_number": null,
					"fulfillment_status": "none"
				}
			],
			"notes": "",
			"phone": "",
			"total": 35,
			"custom": {},
			"currency": "GBP",
			"funnel_id": "fun_IuDsIzSnQiNA2XOpmS",
			"store_id": "store_89QSjazAzPmsUhsIQSNs",
			"customer": {
				"id": "cus_GsGlWiz-Tp1zRTOJf7Dkp",
				"avatar": "//www.gravatar.com/avatar/402c2d5ecacd869e2b977a4f4584d3fa",
				"location": "US, random city",
				"full_name": "Tester Test"
			},
			"payments": [
				{
					"id": "pay_KvHYIzSxNZWnA2XRpHQnF",
					"_id": 2498721,
					"total": 35,
					"source": {
						"payment_gateway": {
							"prototype": {
								"key": "cod"
							}
						}
					},
					"refunds": [],
					"refunded": 0,
					"sub_total": 35,
					"created_at": "a few seconds ago",
					"refundable": 0,
					"discount_snapshot": null,
					"price_bundle_snapshot": [],
                    "cookies": {
                      "otalp_1": "value"
                    }
				}
			],
			"shipping": 0,
			"subtotal": 35,
			"__typename": "Order",
			"account_id": "acc_o5C60ZEzUTDmfB8WXSxnK",
			"created_at": "2024-03-18 14:20:37",
			"refundable": 0,
			"archived_at": null,
			"net_payment": 0,
			"cancelled_at": null,
			"client_details": {
				"ip": "105.158.83.57"
			},
			"discount_value": 0,
			"original_total": 35,
			"billing_address": {
				"zip": "10000",
				"area": "",
				"city": "random city",
				"email": "test@lightfunnels.com",
				"line1": "random address",
				"line2": "",
				"phone": "",
				"state": "random state",
				"country": "US",
				"last_name": "Test",
				"first_name": "Tester"
			},
			"refunded_amount": 0,
			"paid_by_customer": 0,
			"shipping_address": {
				"zip": "10000",
				"area": "",
				"city": "random city",
				"email": "test@lightfunnels.com",
				"line1": "random address",
				"line2": "",
				"phone": "",
				"state": "random state",
				"country": "US",
				"last_name": "Test",
				"first_name": "Tester"
			},
			"shipping_discount": 0,
			"bundle_discount_value": 0,
			"normal_discount_value": 0,
		}
	}

```

---

## Payment events

- `New payment` — *payment/created* — A new payment was created.
- `Paid payment` — *payment/paid* — Paid payment.

#### Payment payload

```
		{
			"node": {
				"id": "pay_fMQN57XdoYOjvy_2m3wfn",
				"items": [
					{
						"id": "vars_MW2k2nbw4q-nlfRUfYgCO",
						"_id": 3050426,
						"sku": "",
						"image": null,
						"price": 35,
						"title": "Test Product",
						"carrier": "",
						"options": [],
						"refund_id": null,
						"__typename": "VariantSnapshot",
						"payment_id": "pay_fMQN57XdoYOjvy_2m3wfn",
						"product_id": "prod_L8WGlMDUfgM6LAivoCZhv",
						"removed_at": null,
						"variant_id": "var_nG3DGrAyPlG2VYqiv2reY",
						"tracking_link": "",
						"custom_options": [],
						"customer_files": [],
						"tracking_number": "",
						"fulfillment_status": "fulfilled",
                        "cookies": {
                          "otalp_1": "value"
                        }
					}
				]
			}
		}

```

---

## Contact events

- `New contact form` — *contact-form/created* — A new contact form was created.

#### Contact form payload

```
		{
			"node":{
				"custom": {},
				"message": "Message goes here",
				"subject": "Subject goes here",
				"email": "no-reply@lightfunnels.com",
				"first_name": "Elhanan",
				"last_name": "Aljoša"
				...
			}
		}

```

- `New signup created` — *contact/signup* — A new sign up was made.
- `Contact updated` — *contact/updated* — An existing customer was updated.

#### Customer payload

```
		{
			"node": {
				"id": "cus_iH3ipbK4yMPPcnKudRRvb",
				"tags": [],
				"email": "Test@lightfunnels.com",
				"leads": [],
				"notes": null,
				"phone": "",
				"avatar": "//www.gravatar.com/avatar/9a7fcb37672ee218b4fc41bba4f7ad8c",
				"custom": {},
				"location": "",
				"full_name": "Random Buyer",
				"last_name": "Buyer",
				"__typename": "Customer",
				"first_name": "Random",
				"billing_address": {
					"zip": "",
					"area": "",
					"city": "",
					"email": "",
					"line1": "",
					"line2": "",
					"phone": "",
					"state": "",
					"country": null,
					"last_name": "",
					"first_name": ""
				},
				"shipping_address": {
					"zip": "",
					"area": "",
					"city": "",
					"email": "",
					"line1": "",
					"line2": "",
					"phone": "",
					"state": "",
					"country": null,
					"last_name": "",
					"first_name": ""
				},
				"accepts_marketing": false
			}
		}

```

---

## Checkout events

- `New checkout` — *checkout/created* — A new checkout was created.
- `Checkout updated` — *checkout/updated* — An existing checkout was updated.

#### Checkout payload

```
		{
			"node":{
				"id": "ch_AfZvYYNDSXdWeXmqKig1C"
			}
		}

```

---

## Product events

- `Product updated` — *product/updated* — An existing product was updated.
- `Product created` — *product/created* — A new product form was created.

#### Product created/updated payload

```
		{
			"node":{
				"id": "prod_tXbZBX43K2pBrmJ9UWTUf",
				"title": "My really great product",
				"description": "My product description"
			}
		}

```

- `Delete product` — *product/deleted* — A product was successfully deleted.

#### Product deleted payload

```
		{
			"node":{
				"id": "prod_tXbZBX43K2pBrmJ9UWTUf",
			}
		}

```

---

## Funnel events

- `Update funnel` — *funnel/updated* — An existing funnel was updated.
- `Create funnel` — *funnel/created* — A new funnel was created.
- `Delete funnel` — *funnel/deleted* — A funnel was successfully deleted.

#### Funnel payload

```
		{
			"node":{
				"id": "fun_KpLWLA-B1QAWKfYj9ZOsz"
			}
		}

```

---

## App events

- `Uninstall app` — *app/uninstalled* — An app was successfully uninstalled.

#### App payload

```
		{
			"node":{
				"id": "id of the account that uninstalled the app"
			}
		}

```

---

## Pagination

This document explains the approach to implement pagination in GraphQL queries, specifically for listing resources such as `funnels`. The pagination is based on cursor-based pagination principles.

### Pagination Query Structure

A GraphQL query for pagination includes parameters for controlling the number of items (`first`), and the point to start fetching items (`after`). Below is a template for a pagination query:

```
{
  "query": "query funnelsQuery(
    $first: Int
    $after: String
    $query: String!
  ) {
    ...funnelsPagination
  }

  fragment funnelsPagination on Query {
    pagination: funnels(first: $first, after: $after, query: $query) {
      edges {
        node {
          id
          name
          slug
          published
          created_at
          updated_at
          share_code
          destinationTemplate {
            uid: id
            id
          }
          currency
          __typename
        }
        cursor
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
",
  "variables": {
    "query": "order_by:id order_dir:desc",
    "first": 25
  }
}

```

#### Query Parameters

- `first`: The number of records to fetch.
- `after`: A cursor, indicating the starting point for fetching records.
- `query`: A query string to filter or sort the data.

#### Response Structure

- `edges`: An array of edge objects, each representing an item.

  - `node`: The actual item with its fields.
  - `cursor`: A unique identifier for the item, used for pagination.

- `pageInfo`: Contains pagination information.

  - `endCursor`: The cursor of the last item in the response.
  - `hasNextPage`: A boolean indicating if there are more items to fetch.

### Implementing Pagination

#### Fetching Initial Data

- Set the `first` parameter to define how many items you want to load initially.
- Leave the `after` parameter empty to start from the beginning.

#### Fetching More Data

- Use the `endCursor` from the `pageInfo` as the `after` value in the next query.
- Check `hasNextPage` before making the next query to ensure there are more items to fetch.

### Example Usage

#### Query for First Page

```
{
  "query": "...",
  "variables": {
    "query": "order_by:id order_dir:desc",
    "first": 25
  }
}

```

#### Query for Subsequent Pages

To fetch subsequent pages, you will need to use the `endCursor` from the previous query's response. Here's how the query should be structured:

```
{
  "query": "...",
  "variables": {
    "query": "order_by:id order_dir:desc",
    "first": 25,
    "after": "[endCursor from previous response]"
  }
}

```

In this query:

- The `first` parameter remains the same, indicating the number of items you want to fetch.
- The `after` parameter is set to the `endCursor` from the previous page's `pageInfo`. This tells the server to start fetching results from the next item after the given cursor.

#### Continuation Logic

When implementing pagination:

1. **Check `hasNextPage`**: Before performing a subsequent query, always check the `hasNextPage` boolean from the `pageInfo` of the current response. If `hasNextPage` is false, there are no more items to fetch.
2. **Update `after` Parameter**: If `hasNextPage` is true, use the `endCursor` as the `after` parameter in your next query.
3. **Repeat Process**: Continue this process to navigate through the pages of data.

### Best Practices

- **Caching**: Consider caching the `endCursor` of each page for a smoother backward navigation experience.
- **Error Handling**: Implement error handling for scenarios where the `endCursor` might be invalid or expired.
- **Performance Considerations**: Monitor the performance impact of large `first` values, as fetching too many items at once can impact server performance.

### Conclusion

Cursor-based pagination in GraphQL is an effective way to handle large datasets. By following the outlined approach and best practices, developers can implement a robust and efficient pagination system in their GraphQL APIs.

---

## Guide to Charging for Your Apps

In this guide, we'll walk you through the process of handling app charges in Lightfunnels.

### Overview

Charging for your apps in Lightfunnels is a straightforward process. Here are the key points to keep in mind:

**One Active Charge Per Account:**

  - At any given time, an app can have only one active charge per user account.

**Automatic Deactivation:**

  - Activating a new charge will automatically deactivate any previous charges associated with the user's account.

**Free Trial Recommendation:**

  - For a positive user experience, it is highly recommended to include a free trial period with your charge.

---

### Create a New App Charge

In this guide, we'll cover the steps to create a charge for your app using GraphQL.

### Step 1: Create a Charge

To create a new charge for your app, you'll need to use the "createAppChargeMutation" GraphQL mutation.

**Explore Mutation Details:**

- Visit [Create App Charges](https://developer.lightfunnels.com/app-charges#create-app-charges) to learn about the "createAppChargeMutation" GraphQL mutation.

### Step 2: Obtain Charge URL

Once you've created the charge, the response will contain a URL. Extract this URL from the response payload.

### Step 3: Redirect User to Accept Charge

Send the user to the obtained charge URL. This can typically be done by redirecting the user's browser to the URL.

### Step 4: Redirect User Upon Charge Acceptance or Denial

Upon the user's acceptance or denial of the charge, they will automatically be redirected to the specified return_url that was provided in the charge creation process.

### Step 5: Check Charge Status Timestamp

Discover the exact moment a user accepts the charge by capturing the timestamp. Otherwise, the `accepted_at` timestamp will be null.

You can retrieve it using the following GraphQL query:

- Visit [App charge query](https://developer.lightfunnels.com/app-charges#get-an-app-charge) to understand the "appCharge" GraphQL query.

---

## Helpful resources

For more detailed information on creating charges or querying app charges, refer to the provided links, Alternatively you can use our provided Postman collection, simply fork it get access to ready to use queries.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/16831799-560b18e3-2697-46e4-9ac7-1933d463fb37?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D16831799-560b18e3-2697-46e4-9ac7-1933d463fb37%26entityType%3Dcollection%26workspaceId%3Dfa9c0249-aba8-4d8f-8378-47dad60c4b51)

If you have further questions or need assistance, contact us at [support@lightfunnels.com](mailto:support@lightfunnels.com).

---

# Part 2 — Resources (Queries & Mutations)

---

## Funnels

These endpoints allow you to retrieve, create, update, and delete Funnel(s).

---

### List all funnels

This query allows you to retrieve a paginated list of all your funnels. By default, a maximum of 25 funnels are shown per page.

#### Arguments

- `query` — *String!* — Supported filter parameters: `order_by` (String) `order_dir` (String) `published` (Boolean) `product_id` (String)
- `after` — *String* — Returns the elements that come after the specified cursor.
- `first` — *String* — Returns up to the first `n` elements from the list.

#### Fields

- [`Funnel!`](https://developer.lightfunnels.com/funnels/types#funnel) — The Funnel! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query FunnelsQuery($first: Int, $after: String, $query: String!){
	funnels(query: "order_by:id order_dir:desc product_id:"15858" published:true", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				_id
				name
				published
				slug
				created_at
			}
			cursor
		}
		pageInfo{
			endCursor
			hasNextPage
		}
	}
}

```

#### Response

```
{
		"data": {
			"edges": [
				{
					"cursor": "WzVE4OTA5LDEe/4OTA5XQ==",
					"node": {
						"id": "VzVE4OTA5LDFR4OTA5XQ==",
						"_id": 14352,
						"slug": "fsnZ8_t3c",
						"name": "My funnel",
						"created_at": "a day ago",
						"published": true,
						"__typename": "Funnel"
					}
				}
			],
			"pageInfo": {
				"endCursor": "WzE5OTY4LDE5OTY4XQ==",
				"hasNextPage": false
			}
		}
	}

```

---

### Create a funnel

This query allows you to add a new funnel.

#### Arguments

- [`InputCreateFunnel!`](https://developer.lightfunnels.com/funnels/types#input-create-funnel) — The InputCreateFunnel! type.

#### Fields

- [`Funnel!`](https://developer.lightfunnels.com/funnels/types#funnel) — The Funnel! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: InputCreateFunnel!) {
	createFunnel(node: $node){
		# Funnel type fields
	}
}

```

#### Response

```
{
		"data": {
			"createFunnel": {
				_id: 2023,
				id: "RnVubmVsOjIwMTIz"
			}
		}
	}

```

---

### Retrieve a funnel

This query allows you to retrieve a funnel by providing its id.

#### Arguments

- `id` — *ID!* — The funnel id.

#### Fields

- [`Funnel!`](https://developer.lightfunnels.com/funnels/types#funnel) — The Funnel! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query FunnelQuery($id: ID!){
		node(id: $id){
			... on Funnel{
				# Funnel type fields
			}
		}
	}

```

#### Response

```
{
		"data": {
			"funnel": {
				"id": "UHJvZHVjdDoxNTUxMQ==",
				"_id": 15511,
				...
			}
		}
	}

```

---

### Update a Funnel

This query allows you to perform an update on a Funnel.

#### Arguments

- `id` — *ID!* — The funnel id.
- `node` — The funnel node.

#### Fields

- [`Funnel!`](https://developer.lightfunnels.com/funnels/types#funnel) — The Funnel! query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateFunnelMutation($node: InputFunnel!, $id: ID!){
		updateFunnel(node: $node, id: $id){
			# Funnel type fields
		}
	}

```

#### Response

```
{
		"data": {
			"funnel": {
				"id": "UHJvZHVjdDoxNTUxMQ==",
				"_id": 15511,
				"name": "My Awesome Funnel",
				...
			}
		}
	}

```

---

### Delete a Funnel

This query allows you to delete funnels.

#### Arguments

- `items` — *[ID!]!* — The funnel ids.

#### Fields

- `[ID]` — List of funnel ids.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	mutation deleteFunnelsMutation($items: [ID!]!){
		deleteFunnels(items: $items){
			# [ID] type fields
		}
	}

```

#### Response

```
{
	"data": {
		"deleteFunnels": [
			"UHJvZHVjdDoxNTUxMQ==",
			"UHJvZHVjdFKWATUxMQ=="
		]
	}
}

```

---

## Stores

These endpoints allow you to retrieve, create, update, and delete Store(s).

---

### List all stores

This query allows you to retrieve all stores on your account.

#### Fields

- [`Store!`](https://developer.lightfunnels.com/stores/types#store) — The Store! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query AccountQuery{
	account{
		stores{
			# Store type fields
			id
			...
		}
	}
}

```

#### Response

```
{
		"data": {
			"account": {
				"stores": [
					{
						"id": "VzVE4OTA5LDFR4OTA5XQ==",
					}
				]
			},
		}
	}

```

---

### Create a store

This query allows you to add a new store.

#### Arguments

- [`StoreInput!`](https://developer.lightfunnels.com/stores/types#store-input) — The StoreInput type.

#### Fields

- `CreateStoreMutation!` — *CreateStoreMutation!* — The CreateStoreMutation! query type. ``` type CreateStoreMutation { account: Account! store: Store! } ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: StoreInput!) {
	createStore(node: $node){
		# CreateStoreMutation type fields
		account {
			id
		}
		store {
			id
		}
		...
	}
}

```

#### Response

```
{
		"data": {
			"createStore": {
				"account": {
					"id": "RnVubmVsOjIwMTIz"
				},
				"store": {
					"id": "RnVubmVsOjIwMTIs"
				}
			}
		}
	}

```

---

### Retrieve a store

This query allows you to retrieve a store by providing its id.

#### Arguments

- `id` — *ID!* — The store id.

#### Fields

- [`Store!`](https://developer.lightfunnels.com/stores/types#store) — The Store! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query StoreQuery($id: ID!){
		node(id: $id){
			... on Store{
				# Store type fields
			}
		}
	}

```

#### Response

```
{
		"data": {
			"node": {
				"id": "UHJvZHVjdDoxNTUxMQ==",
				...
			}
		}
	}

```

---

### Update a Store

This query allows you to perform an update on a Store.

#### Arguments

- `uid` — *ID!* — The store id.
- `node` — The store node.

#### Fields

- [`Store!`](https://developer.lightfunnels.com/stores/types#store) — The Store! query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateStoreMutation($node: StoreUpdateInput!, $id: ID!){
		updateStore(node: $node, id: $id){
			# Store type fields
		}
	}

```

#### Response

```
{
		"data": {
			"updateStore": {
				"id": "UHJvZHVjdDoxNTUxMQ==",
				"name": "My Awesome Store",
				...
			}
		}
	}

```

---

### Delete a Store

This query allows you to delete stores.

#### Arguments

- `items` — *[ID!]!* — The store uids.

#### Fields

- [`Account`](https://developer.lightfunnels.com/account/types#account) — The account type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	mutation deleteStoresMutation($items: [ID!]!){
		deleteStore(items: $items){
			# Account type fields
		}
	}

```

#### Response

```
{
	"data": {
		"deleteStore": {
			# Account type fields
		}
	}
}

```

---

### Add Products to Store

This mutation allows you to add existing products to store.

#### Arguments

- `id` — *[ID!]!* — The store uid.
- `node` — *AddProductsToStoreInput!* — object named node that contains an array of the products uids (see the type structure below).

#### Fields

- `AddProductsToStoreInput!` — *AddProductsToStoreInput!* — The AddProductsToStoreInput! type. ``` type AddProductsToStoreInput { products_uids: [String!]! } ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation addProductsToStore($node: AddProductsToStoreInput!$id: ID!){
    addProductsToStore(id: $id, node: $node) {
      id
      products(cursor: null){
          title
          price
          link
          cursor
      }
    }
  }

```

#### Response

```
{
	"data": {
		"addProductsToStore": {
			# Store type fields
		}
	}
}

```

---

## Products

These endpoints allow you to retrieve, create, update, and delete Product(s).

---

### List all products

This query allows you to retrieve a paginated list of all your products. By default, a maximum of 25 products are shown per page.

#### Arguments

- `query` — *String!* — Supported filter parameters: `order_by` `order_dir` `last_month` `last_week` `last_3_months` `last_year`
- `after` — *String* — Returns the elements that come after the specified cursor.
- `first` — *String* — Returns up to the first `n` elements from the list.

#### Fields

- [`Product!`](https://developer.lightfunnels.com/products/types#product) — The Product query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query productsQuery($first: Int, $after: String, $query: String!){
	products(query: "order_by:id order_dir:desc last_month", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				_id
				title
				price
				thumbnail{
					path(version: version1)
				}
				created_at
			}
			cursor
		}
		pageInfo{
			endCursor
			hasNextPage
		}
	}
}

```

#### Response

```
{
  "data": {
			"edges" : [
				{
					"cursor": "WzVE4OTA5LDEe/4OTA5XQ==",
					"node": {
						"id": "VzVE4OTA5LDFR4OTA5XQ==",
						"price": 10,
						"thumbnail": {
							"id": "SW1hZ2U6NTAyMTQ00",
							"path": "https://assets.lightfunnels.com/...",
							"title": "My beautiful thumbnail"
						},
						"title": "My really great product",
						"__typename": "Product",
						"_id": 14352
					}
				}
			]
		}
}

```

---

### Create a product

This query allows you to add a new product.

#### Arguments

- [`InputProduct!`](https://developer.lightfunnels.com/products/types#input-product) — The InputProduct type.

#### Fields

- [`Product!`](https://developer.lightfunnels.com/products/types#product) — The Product query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: InputProduct!) {
	createProduct(node: $node){
		# Product type fields
	}
}

```

#### Response

```
{
		"data": {
			"createProduct": {
				"id": "UHJvZHVjdDoxNTg1aOA==",
				"_id": 158508,
				"title": "My product",
				"description": "My product description",
				"price": 10,
				"compare_at_price": 21,
			}
		}
	}

```

---

### Retrieve a product

This query allows you to retrieve a product by providing its id.

#### Arguments

- `id` — *ID!* — The product id.

#### Fields

- [`Product!`](https://developer.lightfunnels.com/products/types#product) — The Product query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query productQuery($id: ID!){
		node(id: $id){
			... on Product {
				# Product type fields
			}
		}
	}

```

#### Response

```
{
		"data": {
			"product": {
				"id": "UHJvZHVjdDoxNTUxMQ==",
				"_id": 15511,
				"title": "Awesome Demo Product",
				"description": "This is a dummy product description.",
				"notice_text": "47% Off Today Only",
				"price": 25.75,
				"compare_at_price": 39.99,
				"product_type": "physical_product",
			}
		}
	}

```

---

### Update a Product

This query allows you to perform an update on a Product.

#### Arguments

- `id` — *ID!* — The product id.
- `node` — The product node.

#### Fields

- [`Product!`](https://developer.lightfunnels.com/products/types#product) — The Product query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateProductMutation($node: InputUpdateProduct!, $id: ID!){
		updateProduct(node: $node, id: $id){
			# Product type fields
		}
	}

```

#### Response

```
{
		"data": {
			"updateProduct": {
				"id": "UHJvZHVjdDoxNTUxMQ==",
				"_id": 15511,
				"title": "Awesome Demo Product",
				"description": "This is a dummy product description.",
				"notice_text": "47% Off Today Only",
				...
			}
		}
	}

```

---

### Delete a Product

This query allows you to delete products.

#### Arguments

- `items` — *[ID!]!* — The product ids.

#### Fields

- `[ID]` — List of product ids.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	mutation deleteProductsMutation($items: [ID!]!){
		deleteProducts(items: $items){
			# [ID] type field
		}
	}

```

#### Response

```
{
	"data": {
		"deleteProducts": [
			"UHJvZHVjdDoxNTUxMQ==",
			"UHJvZHVjdFKWATUxMQ=="
		]
	}
}

```

---

## Bundles

These endpoints allow you to retrieve, create, update, and delete Bundle(s).

---

### List all Bundles

This query allows you to retrieve a paginated list of all your Bundles. By default, a maximum of 25 Bundles are shown per page.

#### Arguments

- `query` — *String!* — Supported filter parameters: `order_by` `order_dir`
- `after` — *String* — Returns the elements that come after the specified cursor.
- `first` — *String* — Returns up to the first `n` elements from the list.

#### Fields

- [`PriceBundle!`](https://developer.lightfunnels.com/bundles/types#price-bundle) — The PriceBundle! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query BundlesQuery($first: Int, $after: String, $query: String!){
	priceBundles(query: $query, after: $after, first: $first){
		edges{
			node{
				label
				items {
					label
				}
			}
			cursor
		}
		pageInfo{
			endCursor
			hasNextPage
		}
	}
}

```

#### Response

```
	{
		"data": {
			"priceBundles": {
				"edges": [
					{
							"node": {
									"label": "Test Bundles",
									"items": [
										{
											"label": "Buy 1 item only"
										}
									]
							},
							"cursor": "WyJwYl9WODdGVG4yTTNhYWs5eWg4bVRmR18iLCJwYl9WODdGVG4yTTNhYWs5eWg4bVRmR18iXQ=="
					},
					{
							"node": {
									"label": "Bundle test",
									"items": [
										{
											"label": "Test Bundle"
										}
									]
							},
							"cursor": "WyJwYl9zRVNCYnN3SzQxZWZ4UkpvMHVOZFYiLCJwYl9zRVNCYnN3SzQxZWZ4UkpvMHVOZFYiXQ=="
					},
				],
				"pageInfo": {
					"endCursor": "WyJwYl9GUjFwbzlnWE92ZHd5d1o5SkYtQ3IiLCJwYl9GUjFwbzlnWE92ZHd5d1o5SkYtQ3IiXQ==",
					"hasNextPage": false
				}
			}
		}
	}

```

---

### Create a PriceBundle

This query allows you to add a new PriceBundle.

#### Arguments

- [`InputPriceBundle!`](https://developer.lightfunnels.com/bundles/types#input-price-bundle) — The InputPriceBundle type.

#### Fields

- [`PriceBundle!`](https://developer.lightfunnels.com/bundles/types#price-bundle) — The PriceBundle! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: InputPriceBundle!) {
	createPriceBundle(node: $node){
		id
		label
		items {
			label
			quantity
			discount_value
			discount_type
		}
	}
}

```

#### Response

```
{
		"node" : {
			"label": "Bundle test",
			"items": {
					"label": "Test",
					"quantity": 1,
					"discount_value": 10,
					"discount_type" : "percentage"
			}
		}
	}

```

---

### Retrieve a Bundle

This query allows you to retrieve a PriceBundle by providing its id.

#### Arguments

- `id` — *ID!* — Bundle id.

#### Fields

- [`PriceBundle!`](https://developer.lightfunnels.com/bundles/types#price-bundle) — Bundle query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query BundleQuery($id: ID!){
		node(id: $id){
			... on PriceBundle{
				# PriceBundle type fields
			}
		}
	}

```

#### Response

```
	{
		"data": {
			"node": {
				"created_at": "a few seconds ago",
				"id": "pb_phvLG7yxd4_V3ga-XliGl",
				"label": "Bundle test"
				...
			}
		}
	}

```

---

### Update a PriceBundle

This query allows you to perform an update on a PriceBundle.

#### Arguments

- `id` — *ID!* — Bundle id.
- `node` — Bundle node.

#### Fields

- [`PriceBundle!`](https://developer.lightfunnels.com/bundles/types#price-bundle) — Bundle query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateBundleMutation($node: InputUpdatePriceBundle!, $id: ID!){
		updatePriceBundle(node: $node, id: $id){
			# PriceBundle type fields
		}
	}

```

#### Response

```
{
		"data": {
			"PriceBundle": {
				"created_at": "a few seconds ago",
				"id": "pb_phvLG7yxd4_V3ga-XliGl",
				"label": "Bundle test"
				...
			}
		}
	}

```

---

### Delete a PriceBundle

This query allows you to delete Bundles.

#### Arguments

- `items` — *[ID!]!* — The PriceBundle ids.

#### Fields

- `[ID]` — List of PriceBundle ids.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	mutation deleteBundlesMutation($items: [ID!]!){
		deletePriceBundles(items: $items){
			# [ID] type fields
		}
	}

```

#### Response

```
{
	"data": {
		"deletePriceBundles": [
			"UHJvZHVjdDoxNTUxMQ==",
			"UHJvZHVjdFKWATUxMQ=="
		]
	}
}

```

---

## Collections

These endpoints allow you to retrieve, create, update, and delete Collection(s).

---

### List all collections

This query allows you to retrieve a paginated list of all your collections. By default, a maximum of 25 collections are shown per page.

#### Arguments

- `query` — *String!* — Supported filter parameters: `order_by` `order_dir`
- `after` — *String* — Returns the elements that come after the specified cursor.
- `first` — *String* — Returns up to the first `n` elements from the list.

#### Fields

- [`Collection!`](https://developer.lightfunnels.com/collections/types#collection) — The Collection query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query collectionsQuery($first: Int, $after: String, $query: String!){
	collections(query: "order_by:id order_dir:desc last_month", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				type
				name
				created_at
				...
			}
			cursor
		}
		pageInfo{
			endCursor
			hasNextPage
		}
	}
}

```

#### Response

```
{
		"data": {
			"pagination": {
				"edges": [{
					"node": {
						"id": "col_tDs_sAQZrq9RIrPS-BkyD",
						"type": "specific_funnels",
						"name": "My Collection",
						"created_at": "a few seconds ago",
						"__typename": "Collection"
						...
					},
					"cursor": "W251bGwsImNvbF90RHNfc0FRWnJxOVJJclBTLUJreUQiXQ=="
				}],
				"pageInfo": {
					"endCursor": "W251bGwsImNvbF90RHNfc0FRWnJxOVJJclBTLUJreUQiXQ==",
					"hasNextPage": false
				}
			}
		}
	}

```

---

### Create a collection

This query allows you to add a new collection.

#### Arguments

- [`CollectionInput!`](https://developer.lightfunnels.com/collections/types#collection-input) — The CollectionInput type.

#### Fields

- [`Collection!`](https://developer.lightfunnels.com/collections/types#collection) — The Collection query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: CollectionInput!) {
	createCollection(node: $node){
		# Collection type fields
	}
}

```

#### Response

```
{
		"data": {
			"pagination": {
				"edges": [{
					"node": {
						"id": "col_tDs_sAQZrq9RIrPS-BkyD",
						"type": "specific_funnels",
						"name": "My Collection",
						"created_at": "a few seconds ago",
						"__typename": "Collection"
						...
					},
					"cursor": "W251bGwsImNvbF90RHNfc0FRWnJxOVJJclBTLUJreUQiXQ=="
				}],
				"pageInfo": {
					"endCursor": "W251bGwsImNvbF90RHNfc0FRWnJxOVJJclBTLUJreUQiXQ==",
					"hasNextPage": false
				}
			}
		}
	}

```

---

### Retrieve a collection

This query allows you to retrieve a collection by providing its id.

#### Arguments

- `id` — *ID!* — The collection id.

#### Fields

- [`Collection!`](https://developer.lightfunnels.com/collections/types#collection) — The Collection query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query collectionQuery($id: ID!){
		node(id: $id){
			... on Collection{
				# Collection type fields
			}
		}
	}

```

#### Response

```
{
		"data": {
			"pagination": {
				"edges": [{
					"node": {
						"id": "col_tDs_sAQZrq9RIrPS-BkyD",
						"type": "specific_funnels",
						"name": "My Collection",
						"created_at": "a few seconds ago",
						"__typename": "Collection"
						...
					},
					"cursor": "W251bGwsImNvbF90RHNfc0FRWnJxOVJJclBTLUJreUQiXQ=="
				}],
				"pageInfo": {
					"endCursor": "W251bGwsImNvbF90RHNfc0FRWnJxOVJJclBTLUJreUQiXQ==",
					"hasNextPage": false
				}
			}
		}
	}

```

---

### Update a Collection

This query allows you to perform an update on a Collection.

#### Arguments

- `id` — *ID!* — The collection id.
- `node` — The collection node.

#### Fields

- [`Collection!`](https://developer.lightfunnels.com/collections/types#collection) — The Collection query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateCollectionMutation($node: CollectionUpdateInput!, $id: ID!){
		updateCollection(node: $node, id: $id){
			# Collection type fields
		}
	}

```

#### Response

```
{
		"data": {
			"pagination": {
				"edges": [{
					"node": {
						"id": "col_tDs_sAQZrq9RIrPS-BkyD",
						"type": "specific_funnels",
						"name": "My Collection",
						"created_at": "a few seconds ago",
						"__typename": "Collection"
						...
					},
					"cursor": "W251bGwsImNvbF90RHNfc0FRWnJxOVJJclBTLUJreUQiXQ=="
				}],
				"pageInfo": {
					"endCursor": "W251bGwsImNvbF90RHNfc0FRWnJxOVJJclBTLUJreUQiXQ==",
					"hasNextPage": false
				}
			}
		}
	}

```

---

### Delete a Collection

This query allows you to delete collections.

#### Arguments

- `ids` — *[ID!]!* — The collection ids.

#### Fields

- `[ID]` — List of collection ids.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	mutation deleteCollectionsMutation($ids: [ID!]!){
		deleteCollections(ids: $ids){
			# [ID] type field
		}
	}

```

#### Response

```
{
	"data": {
		"deleteCollections": [
			"UHJvZHVjdDoxNTUxMQ==",
			"UHJvZHVjdFKWATUxMQ=="
		]
	}
}

```

---

## Orders

These endpoints allow you to retrieve, create, update, and delete Order(s).

---

### List all Orders

This query allows you to retrieve a paginated list of all your orders. By default, a maximum of 25 orders are shown per page.

#### Arguments

- `query` — *String!* — Supported filter parameters: `order_by` `order_dir` `status` `financial_status` `fulfillment_status` `created_at` `product_id`
- `after` — *String* — Returns the elements that come after the specified cursor.
- `first` — *String* — Returns up to the first `n` elements from the list.

#### Fields

- [`Order!`](https://developer.lightfunnels.com/orders/types#order) — The Order! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query ordersQuery($first: Int, $after: String, $query: String!){
	orders(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				_id
				name
				total
				fulfillment_status
				financial_status
				customer {
					id
					full_name
				}
				cancelled_at
				date
				test
			}
			cursor
		}
		pageInfo{
			endCursor
			hasNextPage
		}
	}
}

```

#### Response

```
{
		"data": {
			"pagination": {
				"edges": [{
					"node": {
						"id": "order_T3JkZXI6MTgyNTE0",
						"_id": 182514,
						"name": "1608",
						"total": 10,
						"fulfillment_status": "fulfilled",
						"financial_status": "pending",
						"customer": {
							"full_name": "Yassir Ennazk",
							"id": "Q3VzdG9tZXI6MTkxMzUw"
						},
						"cancelled_at": null,
						"date": "3 days ago",
						"test": false,
						"__typename": "Order"
					},
					"cursor": "WzE4MjUxNCwxODI1MTRd"
				}]
			}
		}
	}

```

---

### Retrieve an order

This query allows you to retrieve an order by providing its id.

#### Arguments

- `id` — *ID!* — The order id.

#### Fields

- [`Order!`](https://developer.lightfunnels.com/orders/types#order) — The Order! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query orderQuery($id: ID!){
		node(id: $id){
			... on Order {
				# Order type fields
			}
		}
	}

```

#### Response

```
{
		"data": {
			"order": {
				"id": "order_T3JkZXI6MTgyNTE0",
				"_id": 182514,
				"name": "1608",
				"total": 10,
				"fulfillment_status": "fulfilled",
				"financial_status": "pending"
				...
			}
		}
	}

```

---

### Update an Order

This query allows you to perform an update on an Order.

#### Arguments

- `id` — *ID!* — The order id.
- `node` — The order node.

#### Fields

- [`Order!`](https://developer.lightfunnels.com/orders/types#order) — The Order! query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateOrderMutation($node: InputOrder!, $id: ID!){
		updateOrder(node: $node, id: $id){
			# Order type fields
		}
	}

```

#### Response

```
{
		"data": {
			"order": {
				"id": "order_T3JkZXI6MTgyNTE0",
				"_id": 182514,
				"name": "1608",
				"total": 10,
				"fulfillment_status": "fulfilled",
				"financial_status": "pending"
				...
			}
		}
	}

```

---

### Cancel an Order

This query allows you to perform an cancel an Order.

#### Arguments

- `id` — *ID!* — The order id.
- `reason` — *String!* — The reason for cancelling.
- `notifyCustomer` — *Boolean!* — Notifying the customer about the cancelling.
- `refund` — *Boolean!* — The order refund.

#### Fields

- [`Order!`](https://developer.lightfunnels.com/orders/types#order) — The Order! query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateOrderMutation($id: ID!, $reason: String!, $notifyCustomer: Boolean!, $refund: Boolean!){
		cancelOrder(id: $id, reason: $reason, notifyCustomer: $notifyCustomer, refund: $refund){
			# Order type fields
		}
	}

```

#### Response

```
{
		"data": {
			"order": {
				"id": "order_T3JkZXI6MTgyNTE0",
				"_id": 182514,
				"name": "1608",
				"refunded_amount": 10
				...
			}
		}
	}

```

---

## Customers

These endpoints allow you to retrieve, create, update, and delete Customer(s).

---

### List all Customers

This query allows you to retrieve a paginated list of all your Customers. By default, a maximum of 25 Customers are shown per page.

#### Arguments

- `query` — *String!* — Supported filter parameters: `order_by` `order_dir`
- `after` — *String* — Returns the elements that come after the specified cursor.
- `first` — *String* — Returns up to the first `n` elements from the list.

#### Fields

- [`Customer!`](https://developer.lightfunnels.com/customers/types#customer) — The Customer! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query CustomersQuery($first: Int, $after: String, $query: String!){
	customers(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				_id
				avatar
				full_name
				expenses
				orders_count
				updated_at
				created_at
			}
			cursor
		}
		pageInfo{
			endCursor
			hasNextPage
		}
	}
}

```

#### Response

```
{
		"data": {
			"edges": [{
				"node": {
					"id": "Q3VzdG9tZXI6MTkxMzUw",
					"_id": 191350,
					"avatar": "//www.gravatar.com/avatar/...",
					"full_name": "Yassir Ennazk",
					"expenses": 0,
					"orders_count": 1,
					"updated_at": "an hour ago",
					"created_at": "an hour ago",
					"__typename": "Customer"
				},
				"cursor": "WzE5MTM1MCwxOTEzNTBd"
			}],
			"pageInfo": {
				"endCursor": "WzE0Njk5MSwxNDY5OTFd",
				"hasNextPage": true
			}
		}
	}

```

---

### Create a Customer

This query allows you to add a new Customer.

#### Arguments

- [`InputCustomer!`](https://developer.lightfunnels.com/customers/types#input-customer) — The InputCustomer type.

#### Fields

- [`Customer!`](https://developer.lightfunnels.com/customers/types#customer) — The Customer! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: InputCustomer!) {
	createCustomer(node: $node){
		# Customer type fields
	}
}

```

#### Response

```
{
		"data": {
			"createCustomer": {
				"id": "Q3VzdG9tZXI6MTkxMzUw",
				"_id": 191350,
				"avatar": "//www.gravatar.com/avatar/...",
				"full_name": "Yassir Ennazk",
				...
			}
		}
	}

```

---

### Retrieve a Customer

This query allows you to retrieve a Customer by providing its id.

#### Arguments

- `id` — *ID!* — The Customer id.

#### Fields

- [`Customer!`](https://developer.lightfunnels.com/customers/types#customer) — The Customer! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query CustomerQuery($id: ID!){
		node(id: $id){
			... on Customer{
				# Customer type fields
			}
		}
	}

```

#### Response

```
	{
		"data": {
			"node": {
				"id": "Q3VzdG9tZXI6MTkxMzUw",
				"_id": 191350,
				"avatar": "//www.gravatar.com/avatar/...",
				"full_name": "Yassir Ennazk",
				...
			}
		}
	}

```

---

### Update a Customer

This query allows you to perform an update on a Customer.

#### Arguments

- `id` — *ID!* — The Customer id.
- `node` — The Customer node.

#### Fields

- [`Customer!`](https://developer.lightfunnels.com/customers/types#customer) — The Customer! query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateCustomerMutation($node: InputUpdateCustomer!, $id: ID!){
		updateCustomer(node: $node, id: $id){
			# Customer type fields
		}
	}

```

#### Response

```
{
		"data": {
			"updateCustomer": {
				"id": "Q3VzdG9tZXI6MTkxMzUw",
				"_id": 191350,
				"avatar": "//www.gravatar.com/avatar/...",
				"full_name": "Yassir Ennazk",
				...
			}
		}
	}

```

---

## Discounts

These endpoints allow you to retrieve, create, update, and delete Discount(s).

---

### List all Discounts

This query allows you to retrieve a paginated list of all your Discounts. By default, a maximum of 25 Discounts are shown per page.

#### Arguments

- `query` — *String!* — Supported filter parameters: `order_by` `order_dir`
- `after` — *String* — Returns the elements that come after the specified cursor.
- `first` — *String* — Returns up to the first `n` elements from the list.

#### Fields

- [`Discount!`](https://developer.lightfunnels.com/discounts/types#discount) — The discount query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query DiscountsQuery($first: Int, $after: String, $query: String!){
	discounts(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				code
				value
				type
				usage_limit
				one_time_usage_per_customer
				started_at
				expired_at
				active
				limited_usage
				usage
			}
		}
		pageInfo{
			endCursor
			hasNextPage
		}
	}
}

```

#### Response

```
{
		"data": {
			"edges": [
				{
					"node": {
						"id": "RGlzY291bnQ6MzQw",
						"code": "test discount",
						"value": 15,
						"type": "percentage",
						"usage_limit": 25,
						"one_time_usage_per_customer": false,
						"started_at": "2023-01-03 00:00:00",
						"expired_at": "2023-01-24 00:00:00",
						"active": true,
						"limited_usage": true,
						"usage": 2,
					}
				}
			],
			"pageInfo": {
				"endCursor": "WzE5OTY4LDE5OTY4XQ==",
				"hasNextPage": false
			}
		}
	}

```

---

### Create a Discount

This query allows you to add a new Discount.

#### Arguments

- [`createDiscountMutationInput!`](https://developer.lightfunnels.com/discounts/types#create-discount-mutation-input) — The createDiscountMutationInput type.

#### Fields

- [`Discount!`](https://developer.lightfunnels.com/discounts/types#discount) — The discount query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($input: createDiscountMutationInput!) {
	createDiscount(input: $input){
		# createDiscountMutationPayload
	}
}

```

#### Response

```
{
		"data": {
			"createDiscount": {
				"clientMutationId": "Y291bnQ6MzQw",
				"discount": {
					"id": "RGlzY291bnQ6MzQw",
					"code": "test discount",
					"value": 15,
					"type": "percentage",
					"usage_limit": 25
					...
				}
			}
		}
	}

```

---

### Retrieve a Discount

This query allows you to retrieve a Discount by providing its id.

#### Arguments

- `id` — *ID!* — The Discount id.

#### Fields

- [`Discount!`](https://developer.lightfunnels.com/discounts/types#discount) — The Discount! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query DiscountQuery($id: ID!){
		node(id: $id){
			... on Discount{
				# Discount type fields
			}
		}
	}

```

#### Response

```
	{
		"data": {
			"node": {
				"id": "RGlzY291bnQ6MzQw",
				"code": "test discount",
				"value": 15,
				"type": "percentage",
				"usage_limit": 25
				...
			}
		}
	}

```

---

### Update a Discount

This query allows you to perform an update on a Discount.

#### Arguments

- `input` — The Discount input.

#### Fields

- [`Discount!`](https://developer.lightfunnels.com/discounts/types#discount) — The Discount! query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateDiscountMutation($input: updateDiscountMutationInput!){
		updateDiscount(input: $input){
			# updateDiscountMutationPayload type fields
		}
	}

```

#### Response

```
{
		"data": {
			"updateDiscount": {
				"id": "RGlzY291bnQ6MzQw",
				"code": "test discount",
				"value": 15,
				"type": "percentage",
				"usage_limit": 25
				...
			}
		}
	}

```

---

### Delete a Discount

This query allows you to delete Discounts.

#### Arguments

- `items` — *[ID!]!* — The Discount ids.

#### Fields

- `[ID]` — List of Discount ids.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	mutation deleteDiscountsMutation($items: [ID!]!){
		deleteDiscounts(items: $items){
			# [ID] type fields
		}
	}

```

#### Response

```
{
	"data": {
		"deleteDiscounts": [
			"UHJvZHVjdDoxNTUxMQ==",
			"UHJvZHVjdFKWATUxMQ=="
		]
	}
}

```

---

## Segments

These endpoints allow you to retrieve, create, update, and delete Segment(s).

---

### List all Segments

This query allows you to retrieve a paginated list of all your Segments. By default, a maximum of 25 Segments are shown per page.

#### Arguments

- `query` — *String!* — Supported filter parameters: `order_by` `order_dir`
- `after` — *String* — Returns the elements that come after the specified cursor.
- `first` — *String* — Returns up to the first `n` elements from the list.

#### Fields

- [`Segment!`](https://developer.lightfunnels.com/segments/types#segment) — The Segment! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query SegmentsQuery($first: Int, $after: String, $query: String!){
	segments(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				name
				description
			}
			cursor
		}
		pageInfo{
			endCursor
			hasNextPage
		}
	}
}

```

#### Response

```
{
		"data": {
			"edges": [{
				"node": {
					"id": "U2VnbWVudDozMQ==",
					"name": "Segment test",
					"description": "description ...",
				},
				"cursor": "WzE5MTM1MCwxOTEzNTBd"
			}],
			"pageInfo": {
				"endCursor": "WzE0Njk5MSwxNDY5OTFd",
				"hasNextPage": true
			}
		}
	}

```

---

### Create a Segment

This query allows you to add a new Segment.

#### Arguments

- [`SegmentInput!`](https://developer.lightfunnels.com/segments/types#segment-input) — The SegmentInput type.

#### Fields

- [`Segment!`](https://developer.lightfunnels.com/segments/types#segment) — The Segment! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: SegmentInput!) {
	createSegment(node: $node){
		# Segment type fields
	}
}

```

#### Response

```
{
		"data": {
			"createSegment": {
				"id": "U2VnbWVudDozMQ==",
				"name": "Segment test",
				"description": "description ..."
			}
		}
	}

```

---

### Retrieve a Segment

This query allows you to retrieve a Segment by providing its id.

#### Arguments

- `id` — *ID!* — The Segment id.

#### Fields

- [`Segment!`](https://developer.lightfunnels.com/segments/types#segment) — The Segment! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query SegmentQuery($id: ID!){
		node(id: $id){
			... on Segment {
				# Segment type fields
			}
		}
	}

```

#### Response

```
	{
		"data": {
			"node": {
				"id": "U2VnbWVudDozMQ==",
				"name": "Segment test",
				"description": "description ..."
			}
		}
	}

```

---

### Update a Segment

This query allows you to perform an update on a Segment.

#### Arguments

- `id` — *Int!* — The Segment id.
- `node` — The Segment node.

#### Fields

- [`Segment!`](https://developer.lightfunnels.com/segments/types#segment) — The Segment! query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateSegmentMutation($node: SegmentInput!, $id: ID!){
		updateSegment(node: $node, id: $id){
			# Segment type fields
		}
	}

```

#### Response

```
{
		"data": {
			"updateSegment": {
				"id": "U2VnbWVudDozMQ==",
				"name": "Segment test",
				"description": "description ..."
			}
		}
	}

```

---

### Delete a Segment

This query allows you to delete Segments.

#### Arguments

- `items` — *[ID!]!* — The Segment ids.

#### Fields

- `[ID]` — List of segment ids.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	mutation deleteSegmentsMutation($items: [ID!]!){
		deleteSegments(items: $items){
			# [ID] type fields
		}
	}

```

#### Response

```
{
	"data": {
		"deleteSegments": [
			"UHJvZHVjdDoxNTUxMQ==",
			"UHJvZHVjdFKWATUxMQ=="
		]
	}
}

```

---

## Reviews

These endpoints allow you to retrieve, create, update, and delete Review(s).

---

### List all reviews

This query allows you to retrieve a paginated list of all your reviews. By default, a maximum of 25 reviews are shown per page.

#### Arguments

- `query` — *String!* — Supported filter parameters: `order_by` `order_dir` `product_id`
- `after` — *String* — Returns the elements that come after the specified cursor.
- `first` — *String* — Returns up to the first `n` elements from the list.

#### Fields

- [`Review!`](https://developer.lightfunnels.com/reviews/types#review) — The Review query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query reviewsQuery($first: Int, $after: String, $query: String!){
	reviews(query: "order_by:id order_dir:desc last_month", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				_id
				name
				email
				content
				rate
				published
				avatar
				created_at
				updated_at
				...
			}
			cursor
		}
		pageInfo{
			endCursor
			hasNextPage
		}
	}
}

```

#### Response

```
{
		"data": {
			"pagination": {
				"edges": [{
					"node": {
						"id": "UmV2aWV3OjQ4NDUy",
						"_id": 48452,
						"name": "Yassir Ennazk",
						"email": "Yassir@lightfunnels.com",
						"content": "some text",
						"rate": 5,
						"published": true,
						"avatar": "//www.gravatar.com/avatar/...",
						"created_at": "a few seconds ago",
						"updated_at": "a few seconds ago",
						"__typename": "Review"
						...
					},
					"cursor": "WzQ4NDUyLDQ4NDUyXQ=="
				}],
				"pageInfo": {
					"endCursor": "WzQ4NDUyLDQ4NDUyXQ==",
					"hasNextPage": false
				}
			}
		}
	}

```

---

### Create a review

This query allows you to add a new review.

#### Arguments

- `product_id` — *ID!* — The review product id.
- [`InputReview!`](https://developer.lightfunnels.com/reviews/types#input-review) — The InputReview type.

#### Fields

- [`Review!`](https://developer.lightfunnels.com/reviews/types#review) — The Review query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($product_id: ID!, $node: InputReview!) {
	createReview(product_id: $product_id, node: $node){
		# Review type fields
	}
}

```

#### Response

```
{
		"data": {
			"pagination": {
				"edges": [{
					"node": {
						"id": "UmV2aWV3OjQ4NDUy",
						"name": "Yassir Ennazk",
						"email": "Yassir@lightfunnels.com",
						"content": "some text",
						...
					},
					"cursor": "WzQ4NDUyLDQ4NDUyXQ=="
				}],
				"pageInfo": {
					"endCursor": "WzQ4NDUyLDQ4NDUyXQ==",
					"hasNextPage": false
				}
			}
		}
	}

```

---

### Retrieve a review

This query allows you to retrieve a review by providing its id.

#### Arguments

- `id` — *ID!* — The review id.

#### Fields

- [`Review!`](https://developer.lightfunnels.com/reviews/types#review) — The Review query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	query reviewQuery($id: ID!){
		node(id: $id){
			... on Review {
				# Review type fields
			}
		}
	}

```

#### Response

```
{
		"data": {
			"pagination": {
				"edges": [{
					"node": {
						"id": "UmV2aWV3OjQ4NDUy",
						"name": "Yassir Ennazk",
						"email": "Yassir@lightfunnels.com",
						"content": "some text",
						...
					},
					"cursor": "WzQ4NDUyLDQ4NDUyXQ=="
				}],
				"pageInfo": {
					"endCursor": "WzQ4NDUyLDQ4NDUyXQ==",
					"hasNextPage": false
				}
			}
		}
	}

```

---

### Update a Review

This query allows you to perform an update on a Review.

#### Arguments

- `id` — *ID!* — The review id.
- `node` — The review node.

#### Fields

- [`Review!`](https://developer.lightfunnels.com/reviews/types#review) — The Review query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateReviewMutation($node: InputUpdateReview!, $id: ID!){
		updateReview(node: $node, id: $id){
			# Review type fields
		}
	}

```

#### Response

```
{
		"data": {
			"pagination": {
				"edges": [{
					"node": {
						"id": "UmV2aWV3OjQ4NDUy",
						"name": "Yassir Ennazk",
						"email": "Yassir@lightfunnels.com",
						"content": "some text",
						...
					},
					"cursor": "WzQ4NDUyLDQ4NDUyXQ=="
				}],
				"pageInfo": {
					"endCursor": "WzQ4NDUyLDQ4NDUyXQ==",
					"hasNextPage": false
				}
			}
		}
	}

```

---

### Delete a Review

This query allows you to delete reviews.

#### Arguments

- `items` — *[ID!]!* — The review ids.

#### Fields

- `[ID]` — List of review ids.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	mutation deleteReviewsMutation($items: [ID!]!){
		deleteReviews(items: $items){
			# [ID] type field
		}
	}

```

#### Response

```
{
	"data": {
		"deleteReviews": [
			"UHJvZHVjdDoxNTUxMQ==",
			"UHJvZHVjdFKWATUxMQ=="
		]
	}
}

```

---

## Account settings

These endpoints allow you to retrieve, update your Account settings.

---

### Retrieve account pixels

- `facebook_pixels` — *[Pixel!]!* — The account facebook_pixels. ``` type Pixel { label: String! value: String! } ```
- `snapchat_pixels` — *[Pixel!]!* — The account snapchat_pixels. ``` type Pixel { label: String! value: String! } ```
- `tiktok_pixels` — *[Pixel!]!* — The account tiktok_pixels. ``` type Pixel { label: String! value: String! } ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query AccountQuery{
  account {
    facebook_pixels {
      label
      value
    }
    snapchat_pixels {
      label
      value
    }
    tiktok_pixels {
      label
      value
    }
  }
}

```

#### Response

```
{
  "data": {
    "account": {
      "facebook_pixels": [
        {
          "label": "My fb pixel",
          "value": "Some pixel value"
        }
      ],
      ...
    }
  }
}

```

---

### Update account pixels

#### Fields

- `facebook_pixels` — *[InputPixel]* — The account facebook pixels. ``` input InputPixel { label: String! value: String! } ```
- `snapchat_pixels` — *[InputPixel]* — The account snapchat pixels. ``` input InputPixel { label: String! value: String! } ```
- `tiktok_pixels` — *[InputPixel]* — The account tiktok pixels. ``` input InputPixel { label: String! value: String! } ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation InputUpdateAccount($node: InputUpdateAccount!){
  updateAccount(node: $node) {
    id
    facebook_pixels {
      label
      value
    }
    snapchat_pixels {
      label
      value
    }
    tiktok_pixels {
      label
      value
    }
    ...
  }
}

Variables example:

{
  facebook_pixels: [
    {
      label: 'My fb px label',
      value: 'the actual pixel'
    }
  ],
  snapchat_pixels: [
    {
      label: 'My sn px label',
      value: 'the actual pixel'
    }
  ],
  tiktok_pixels: [
    {
      label: 'My tk px label',
      value: 'the actual pixel'
    }
  ]
}

```

#### Response

```
{
  "data": {
    "account": {
      "facebook_pixels": [
        {
          "label": "My fb pixel",
          "value": "Some pixel value"
        }
      ],
      ...
    }
  }
}

```

---

### Create Facebook Conversion API Integration

#### Arguments

- `node` — *FacebookConversionApi!* — Account facebook conversion API integration. ``` input FacebookConversionApi { token: String! label: String! pixels: [String!]! } ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation CreateConversionApi($node: FacebookConversionApi!){
  createConversionApiFacebookIntegration(node: $node) {
    id
    ...
  }
}

Variables example:
{
  "node": {
    "label": "My capi integration",
    "token": "your facebook token",
    "pixels": ["pixel_1", "pixel_2"]
  }
}

```

#### Response

```
{
  "data": {
    "account": {
      "node": [
        {
          "id": "Your account ID"
        }
      ],
      ...
    }
  }
}

```

---

### Retrieve Integrations

- `integrations` — *[Integration!]!* — Account integrations. ``` type Integration implements Node { id: ID! platform: String! label: String! details: IntegrationDetails } scalar IntegrationDetails ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query AccountQuery{
  account {
    integrations {
      id
      label
      platform
      details
    }
  }
}

```

#### Response

```
{
  "data": {
    "account": {
      "integrations": [
        {
          "id": "integration id",
          "label": "testcapi",
          "platform": "facebook"
          "details": {
            "pixels": ["some pixel id"]
          },
        }
      ]
      ...
    }
  }
}

```

---

### Remove Integration

#### Arguments

- `id` — *ID!* — Account integration id.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation removeIntegrationMutation($id: ID!){
  removeIntegration(id: $id){
    id
    integrations{
      id
    }
  }
}

Variables example:
{
  "id": "integration id"
}

```

#### Response

```
{
  "data": {
    "account": {
      "id": "Your account ID",
      "integrations": [
        {
          "id": "integration id 1"
        },
        {
          "id": "integration id 2"
        }
      ]
      ...
    }
  }
}

```

---

## Shipping Rate Groups

These endpoints allow you to retrieve, create, update, and delete shipping rate group(s) --- used to specify the shipping rates for geographical zone, and can be then connected to a product or a store (see update mutations for those data structures).

---

### List

This query allows you to retrieve all shipping rate groups on your account.

#### Fields

- `[[ShippingRateGroup!]!](https://developer.lightfunnels.com/shipping-rate-groups/types#shipping-rate-group)` — The ShippingRateGroup! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query AccountQuery{
	account{
		shipping_rates {
			# ShippingRateGroup type fields
			id
			...
		}
	}
}

```

#### Response

```
{
		"data": {
			"account": {
				"shipping_rates": [
					{
						"id": "shrg_qsdqsdqsdsqdqs",
					}
				]
			},
		}
	}

```

---

### Create

This query allows you to create a new shipping rate group.

#### Arguments

- [`InputShippingRateGroup!`](https://developer.lightfunnels.com/shipping-rate-groups/types#input-shipping-rate-group) — The InputShippingRateGroup! type.

#### Fields

- `CreateShippingRateGroupMutation!` — *CreateShippingRateGroupMutation!* — The CreateShippingRateGroupMutation! query type. ``` type CreateShippingRateGroupMutation { node: InputShippingRateGroup! } ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: InputShippingRateGroup!) {
	createShippingRateGroup(node: $node){
		# Account type fields
		id
		...
	}
}

```

#### Response

```
{
		"data": {
			"createShippingRateGroup": {
				# Account type fields
                "id" : "acc_RnVubmVsOjIwMTIz"
			}
		}
	}

```

---

### Update

This mutation allows you to perform an update on a shipping rate group.

#### Arguments

- `id` — *ID!* — The shipping rate group id.
- `node` — The shipping rate group input node.

#### Fields

- [`ShippingRateGroup!`](https://developer.lightfunnels.com/shipping-rate-groups/types#shipping-rate-group) — The ShippingRateGroup! query type.

#### Request
Posthttps://services.lightfunnels.com/api/v2

```
mutation updateShippingRateGroupMutation($node: InputShippingRateGroup!, $id: ID!){
		updateShippingRateGroup(node: $node, id: $id){
			# ShippingRateGroup type fields
		}
	}

```

#### Response

```
{
		"data": {
			"updateShippingRateGroup": {
				"id": "shrg_qsdqsdqsdsqdqs",
				...
			}
		}
	}

```

---

### Delete

This mutation allows you to delete a shipping rate group.

#### Arguments

- `uid` — *ID!* — The shipping rate group id.

#### Fields

- [`Account`](https://developer.lightfunnels.com/account/types#account) — The account type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	mutation deleteShippingRateGroupMutation($id: ID!){
		deleteShippingRateGroup(id: $id){
			# Account type fields
		}
	}

```

#### Response

```
{
	"data": {
		"deleteShippingRateGroup": {
			# Account type fields
            "id" : "acc_RnVubmVsOjIwMTIz"
		}
	}
}

```

---

## App charges

In this guide, we will look at how to handle charges for your app in Lightfunnels.

---

### Create app charges

To create an app charge, you need to use the following GraphQL mutation:

#### Arguments

- [`createAppChargeInput!`](https://developer.lightfunnels.com/app-charges/types#create-app-charge-input) — The createAppChargeInput! type.

#### Fields

- [`createAppChargePayload`](https://developer.lightfunnels.com/app-charges/types#create-app-charge-input-payload) — The createAppChargePayload type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
## Mutation
mutation createAppChargeMutation($input: createAppChargeInput!) {
	createAppCharge(input: $input) {
		createAppChargePayload type fields
	}
}

```

#### createAppChargeInput type example

```
{
	"input": {
		"node": {
			"price": 0,
			"return_url": "https://your-website.com",
			"name": "Plan name",
			"trial": 0,
			"plan_id": "navigate to your app billing tab and select a plan id under app plans"
		}
	}
}

```

#### createAppChargePayload type example

```
{
		"node": {
			"appCharge": {
				"id": "charge id",
				"price": 25.99,
				"name": "basic",
				"started_at": "2024-01-12 15:56:23"
			},
		}
	}

```

---

### List all app charges

To get your app charges, you need to use the following GraphQL query:

#### Arguments

appCharges query has no arguments

#### Fields

- [`AppCharges!`](https://developer.lightfunnels.com/app-charges/types#app-charges) — The AppCharges! query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query {
	appCharges{
		list {
			id
			price
			name
			started_at
		}
	}
}

```

#### Response

```
	{
		"appCharges": {
			"id": "charge id",
			"price": 25.99,
			"name": "basic",
			"started_at": "2024-01-12 15:56:23"
		}
	}

```

---

### Get an app charge

To get an app charge, you need to use the following GraphQL query:

#### Arguments

- `id` — *ID!* — The app charge id.

#### Fields

- [`AppCharge`](https://developer.lightfunnels.com/app-charges/types#app-charge) — The AppCharge query type.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query appChargeQuery($id: ID!) {
	appCharge(id: $id){
		id
		price
		name
		started_at
	}
}

```

#### Response

```
	{
		"appCharge": {
			"id": "charge id",
			"price": 25.99,
			"name": "basic",
			"started_at": "2024-01-12 15:56:23"
		}
	}

```

---

# Part 3 — GraphQL Types

---

## Funnels Types

This list contains all query types for the funnel endpoints.

---

### Funnel

#### Fields

- `id` — *ID!* — Unique identifier for the funnel.
- `uid` — *ID!* — Unique identifier for the funnel.
- `_id` — *Int!* — Unique numeral identifier for the funnel.
- `name` — *String!* — The funnel name.
- `slug` — *String!* — The funnel slug.
- `starting_step_id` — *ID* — The funnel starting step id.
- `published` — *Boolean!* — The funnel published option.
- `record` — *Boolean!* — The funnel record option.
- `enable_address_autocomplete` — *Boolean!* — The funnel enable address autocomplete option.
- `fire_lead_insteadof_purchase` — *Boolean!* — The funnel fire lead instead of purchase option.
- `share_code` — *String* — The funnel share code.
- `styles` — *[StepStyle!]* — The funnel styles. ``` input StepStyle { key: String! name: String! type: String! value: FunnelStyleValue } ``` ``` scalar FunnelStyleValue ```
- `active_payment_methods` — The funnel active payment method.
- `active_facebook_pixels` — *[String!]!* — The funnel active facebook pixels.
- `active_tiktok_pixels` — *[String!]!* — The funnel active tiktok pixels.
- `active_snapchat_pixels` — *[String!]!* — The funnel active snapchat pixels.
- `activate_google_analytics` — *Boolean!* — The funnel activate google analytics option.
- `transform` — *Transform!* — The funnel transform. ``` type Transform { y: Float! x: Float! k: Float! } ```
- `updated_at` — Timestamp of when the funnel was updated.
- `created_at` — Timestamp of when the funnel was created.
- `template` — Funnel template.
- `destinationTemplate` — Funnel destination template.
- `preferred_domain` — The funnel preferred domain.
- `preferred_domain_id` — *ID* — The funnel preferred domain id.
- `favicon` — The funnel favicon.
- `favicon_id` — *ID* — The funnel favicon id.
- `default_language` — *FunnelLanguage!* — The funnel default language. ``` scalar FunnelLanguage ```
- `languages` — *[FunnelLanguage!]!* — The funnel languages. ``` scalar FunnelLanguage ```
- `steps` — The funnel steps.
- `statistics` — The funnel statistics. ``` # Arguments startDate: String endDate: String ```
- `header_scripts` — *String* — The funnel header scripts.
- `ignore_invalide_phones` — *Boolean!* — The funnel ignore invalid phones option.
- `store` — The funnel store.
- `currency` — *String* — The funnel currency.
- `currency_format` — *String* — The funnel currency format.
- `smart_sections` — *[SmartSection!]!* — The funnel smart sections. ``` type SmartSection { reference_id: ID! name: String! thumbnail: VirtualImage2! body: BuilderNode! } ``` ``` type VirtualImage2 { key: String url: String } scalar BuilderNode ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query FunnelsQuery($first: Int, $after: String, $query: String!){
	funnels(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				_id
				name
				published
				slug
				created_at
				...
			}
		}
	}
}

```

---

### InputCreateFunnel

#### Fields

- `funnel_steps` — The funnel steps.
- `style_id` — *ID* — The funnel style id.
- `product_id` — *ID* — The funnel product id.
- `name` — *String!* — The funnel name.
- `slug` — *String!* — The funnel slug.
- `currency` — *String* — The funnel currency.
- `lang` — *FunnelLanguage!* — The funnel language. ``` scalar FunnelLanguage ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: InputCreateFunnel! {
	createFunnel(node: $node){
		# Funnel type fields
	}
})

```

---

### InputFunnel

#### Fields

- `name` — *String* — The funnel name.
- `slug` — *String* — The funnel slug.
- `starting_step_uid` — *ID* — The funnel starting step uid.
- `favicon_id` — *ID* — The funnel favicon id.
- `steps` — The funnel steps.
- `deleted_steps` — *[ID!]* — The funnel deleted steps.
- `published` — *Boolean* — The funnel published option.
- `record` — *Boolean* — The funnel record option.
- `fire_lead_insteadof_purchase` — *Boolean* — The funnel fire lead instead of purchase option.
- `enable_address_autocomplete` — *Boolean* — The funnel enable address autocomplete option.
- `header_scripts` — *String* — The funnel header scripts.
- `preferred_domain_uid` — *String* — The funnel preferred domain uid.
- `active_payment_methods` — *[ActivePaymentMethod!]* — The funnel active payment method. ``` input ActivePaymentMethod { settings: FunnelPaymentGatewaySettings! id: Int! } ``` ``` scalar FunnelPaymentGatewaySettings ```
- `active_facebook_pixels` — *[String!]* — The funnel active facebook pixels.
- `active_tiktok_pixels` — *[String!]* — The funnel active tiktok pixels.
- `active_snapchat_pixels` — *[String!]* — The funnel active snapchat pixels.
- `activate_google_analytics` — *Boolean* — The funnel activate google analytics option.
- `transform` — *InputTransform* — The funnel transform. ``` input InputTransform { y: Float! x: Float! k: Float! } ```
- `styles` — *[InputStepStyle!]* — The funnel styles. ``` input InputStepStyle { key: String! name: String! type: String! value: FunnelStyleValue } ```
- `default_language` — *FunnelLanguage* — The funnel default language. ``` scalar FunnelLanguage ```
- `languages` — *[FunnelLanguage!]* — The funnel languages. ``` scalar FunnelLanguage ```
- `ignore_invalide_phones` — *Boolean* — The funnel ignore invalid phones option.
- `currency` — *String* — The funnel currency.
- `currency_format` — *String* — The funnel currency format.
- `smart_sections` — *[SmartSectionInput!]* — The funnel smart sections. ``` type SmartSectionInput { reference_id: ID! name: String! thumbnail: VirtualImage2! body: BuilderNode! } ``` ``` type VirtualImage2 { key: String url: String } scalar BuilderNode ```
- `reset_translations` — *Boolean* — The funnel reset translations boolean.
- `activate_google_tag_manager_id` — *Boolean* — Activate google tag manager id boolean.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation updateFunnelMutation($node: InputFunnel!, $id: Int!){
	updateFunnel(node: $node, id: $id){
		# Funnel type fields
	}
}

```

---

### InputUpdateStep

#### Fields

- `id` — *ID!* — The funnel unique identifier.
- `product_uid` — *ID!* — The funnel product uid.
- `slug` — *String!* — The funnel slug.
- `visual` — *InputStepVisual* — The funnel visual. ``` input InputStepVisual { x: Float y: Float } ```
- `title` — *String!* — The funnel title.
- `type` — The funnel step type.

---

### FunnelPaymentGateway

#### Fields

- `index` — *Int!* — The funnel index.
- `payment_gateway_id` — *ID!* — The funnel payment gateway id.
- `payment_gateway` — The funnel payment gateway.
- `settings` — *FunnelPaymentGatewaySettings!* — The funnel product id. ``` scalar FunnelPaymentGatewaySettings ```

---

### Step

#### Fields

- `id` — *ID!* — Unique identifier for the funnel step.
- `uid` — *ID!* — Unique identifier for the funnel step.
- `_id` — *Int!* — Unique numeral identifier the funnel step.
- `slug` — *String!* — The funnel step slug.
- `title` — *String!* — The funnel step title.
- `type` — The funnel step type.
- `visual` — *StepVisual!* — The funnel step visual. ``` type StepVisual { x: Float! y: Float! } ```
- `settings` — *StepSettings!* — The funnel step settings. ``` scalar StepSettings ```
- `product_id` — *ID* — The funnel step product id.
- `funnel` — *Funnel* — The funnel type.
- `thumbnail` — *VirtualImage2* — The funnel step thumbnail.
- `body` — *StepBody* — The funnel step body.
- `disable_token_redirection` — *Boolean!* — The funnel step disable token redirection.
- `meta` — *StepMeta!* — The funnel step disable token redirection.
- `updated_at` — Timestamp of when the image was updated.
- `created_at` — Timestamp of when the image was created.

---

### InputStep

#### Fields

- `product_id` — *ID* — The funnel product id.
- `slug` — *String!* — The funnel step slug.
- `visual` — *InputStepVisual* — The funnel visual. ``` input InputStepVisual { x: Float y: Float } ```
- `title` — *String!* — The funnel step title.
- `type` — The funnel step type.
- `settings` — *StepSettings!* — The funnel step settings. ``` scalar StepSettings ```
- `body` — *StepBody* — The funnel step body. ``` scalar StepBody ```
- `disable_token_redirection` — *Boolean* — The funnel disable token redirection option.
- `thumbnail` — *String* — The funnel thumbnail.
- `template` — *GeniricStepTemplate* — The funnel template. ``` enum GeniricStepTemplate { blank contact_us privacy_policy refund_policy terms_of_service } ```

---

### FunnelConnection

#### Fields

- `pageInfo` — *PageInfo!* — Funnel connection page info. ``` type PageInfo { hasNextPage: Boolean! hasPreviousPage: Boolean! startCursor: String endCursor: String } ```
- `edges` — *[FunnelEdge]* — The Funnel connection edges. ``` type FunnelEdge { node: Funnel cursor: String! } ```
- `count` — *Int!* — The Funnel connection count.

---

### StepType

```
enum StepType {
	blank_page
	product_page
	checkout_page
	upsell_page
	downsell_page
	split_test
	article_page
	squeeze_page
	thank_you_page
	generic_page
	home_page
	collection_page
}

```

---

### FunnelStatistics

- `steps` — Funnel statistics steps

### StepStatistics

- `id` — *String!* — Unique identifier for the funnel step statistics.
- `visits` — *Int!* — Funnel visits
- `clicks` — *Int!* — Funnel clicks
- `ctr` — *Float!* — Funnel click through rate
- `links` — Funnel step links

### StepLinkState

- `id` — *String!* — Unique identifier for the funnel step link state.
- `visits` — *Int!* — Funnel visits
- `ctr` — *Float!* — Funnel click through rate
- `cvr` — *Float!* — Funnel conversion rate

---

### Template

- `id` — *ID!* — Unique identifier for the funnel template.
- `uid` — *ID!* — Unique identifier for the funnel template.
- `_id` — *Int!* — Unique numeral identifier for the funnel template.
- `name` — *String!* — Funnel template name
- `thumbnail` — *String!* — Funnel template thumbnail
- `updated_at` — Timestamp of when the funnel template was updated.
- `created_at` — Timestamp of when the funnel template was created.
- `pages` — Funnel template pages
- `mobile_thumbnail` — *String!* — Funnel template mobile thumbnail
- `desktop_thumbnail` — *String!* — Funnel template desktop thumbnail
- `price` — *Float!* — Funnel template price
- `description` — *String!* — Funnel template description
- `tags` — *[String!]!* — Funnel template tags
- `features` — *[Feature!]!* — Funnel template features ``` type Feature { id: ID! image: String! title: String! description: String! } ```
- `likes` — *Int!* — Funnel template likes
- `isLiked` — *Boolean* — Funnel template isLiked boolean
- `languages` — *[FunnelLanguage!]!* — Funnel template languages ``` scalar FunnelLanguage ```

### TemplatePage

- `id` — *ID!* — Unique identifier for the funnel template page.
- `_id` — *Int!* — Unique numeral identifier for the funnel template page.
- `url` — *String!* — Funnel template page url
- `name` — *String!* — Funnel template page name
- `type` — *StepType!* — Funnel template page type ``` enum StepType { blank_page product_page checkout_page upsell_page downsell_page split_test article_page squeeze_page thank_you_page generic_page home_page collection_page } ```

---

## Stores Types

This list contains all query types for the store endpoints.

---

### Store

#### Fields

- `id` — *ID!* — Unique identifier for the store.
- `uid` — *ID!* — Unique identifier for the store.
- `name` — *String!* — The store name.
- `slug` — *String!* — The store slug.
- `refund_policy` — *String* — The store refund policy.
- `privacy_policy` — *String* — The store privacy policy.
- `terms_of_services` — *String* — The store terms of services.
- `single_checkout_page` — *Boolean!* — The store single checkout page boolean.
- `funnel` — The store funnel.
- `default_collection_id` — *ID!* — The store default collection id.
- `shipping_group_id` — *String* — The store shipping group id.
- `collections` — The store collections.
- `defaultDomain` — *String!* — The store default domain.
- `address` — *String!* — The store address.
- `legal_name` — *String!* — The store legal name.
- `email` — *String!* — The store email.
- `products` — The store products. ``` Arguments cursor: String ```

---

### StoreInput

#### Fields

- `name` — *String!* — The store name.
- `slug` — *String!* — The store slug.
- `style_id` — *ID* — The store style id.
- `currency` — *String* — The store currency.
- `single_checkout_page` — *Boolean* — The store single checkout page boolean.
- `lang` — *FunnelLanguage!* — The store language. ``` scalar FunnelLanguage ```

---

### StoreUpdateInput

#### Fields

- `style_uid` — *ID* — The store style uid.
- `shipping_group_uid` — *String* — The store shipping group uid.
- `collections_uids` — *[ID!]* — The store collections uids.
- `refund_policy` — *String* — The store refund policy.
- `privacy_policy` — *String* — The store privacy policy.
- `terms_of_services` — *String* — The store terms of services.
- `address` — *String* — The store address.
- `legal_name` — *String* — The store legal name.
- `single_checkout_page` — *Boolean* — The store single checkout page.
- `email` — *String* — The store email.
- `slug` — *String* — The store slug.

---

## Products Types

This list contains all query and inputs types for the product endpoints.

---

### Product

#### Fields

- `id` — *ID!* — Unique identifier for the product.
- `_id` — *Int!* — Unique number identifier for the product.
- `uid` — *ID!* — Unique identifier for the product.
- `updated_at` — Timestamp of when the product was updated.
- `created_at` — Timestamp of when the product was created.
- `title` — *String!* — The product title.
- `slug` — *String!* — The product slug.
- `description` — *String* — The product description.
- `price` — *Float!* — The product price.
- `compare_at_price` — *Float!* — The product compare price.
- `images` — The product images.
- `images_ids` — *[ID!]!* — The product image ids.
- `options` — The product options.
- `variants` — The product variants.
- `custom_options` — The product custom options.
- `enable_custom_options` — *Boolean!* — The product enable custom options boolean option.
- `default_variant` — The product default variants.
- `query` — String! — the reviews query string.
- `tags` — A list of tags associated with the product. Tags are useful for categorizing and filtering products.
- `review_score` — *Float!* — The product review score.
- `review_count` — *Int!* — The product review count.
- `thumbnail` — The product thumbnail.
- `order_bump` — The product order bump.
- `features` — The product features.
- `testimonials` — */products/types#product-testimonials* — The product testimonials.
- `faq` — *[ProductFaq!]!* — The product faq. ``` type ProductFaq { id: String! question: String! answer: String! } ```
- `notice_text` — *String!* — The product notice text.
- `product_type` — *ProductType!* — The product type. ``` enum ProductType { physical_product digital_product } ```
- `default_variant_id` — *ID!* — The product default variant id.
- `shipping_group_id` — *ID* — The product shipping group id.
- `price_bundle_id` — *ID* — The product price bundle id.
- `price_bundle` — The product price bundle.
- `file` — The product file.
- `file_id` — *ID* — The product file id.
- `sku` — *String!* — The product sku.
- `crossSellProducts` — The product cross sell products.
- `funnels` — *[Funnel!]!* — The product funnels.
- `stores` — *[Store!]!* — The product stores.
- `collections_ids` — *[ID!]!* — The product collections ids.
- `customFunnel` — The product custom funnel.
- `enable_inventory_limit` — *Boolean!* — The product enable inventory limit.
- `inventory_quantity` — *Int!* — The product inventory quantity.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query productsQuery($first: Int, $after: String, $query: String!){
	products(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				_id
				title
				price
				thumbnail{
					path(version: version1)
				}
				created_at
				...
			}
		}
	}
}

```

---

### ProductOption

#### Fields

- `id` — *String!* — Unique identifier for the product option.
- `label` — *String!* — The product label.
- `options` — *[String!]!* — The product options.
- `type` — *ProductOptionTypeEnum!* — The product type. ``` enum ProductOptionTypeEnum { image text color } ```
- `options_types` — *[ProductOptionType!]!* — The product options types. ``` type ProductOptionType { option_id: String! value: ProductOptionTypeValue! } scalar ProductOptionTypeValue ```

---

### InputProduct

#### Fields

- `title` — *String!* — The product title.
- `description` — *String* — The product description.
- `price` — *Float* — The product price.
- `sku` — *String* — The product sku.
- `slug` — *String* — The product slug.
- `compare_at_price` — *Float* — The product compare price.
- `options` — The product options.
- `images` — *[ID!]* — The product images.
- `variants` — The product variants.
- `tags` — *[ID!]* — The product tags.
- `order_bump` — The product order bump.
- `features` — *[InputProductFeatures!]* — The product features. ``` input InputProductFeatures { id: String! title: String! description: String! image_id: ID } ```
- `testimonials` — *[InputProductTestimonials!]* — The product testimonials. ``` input InputProductTestimonials { id: String! name: String! position: String! comment: String! image_id: ID } ```
- `countdown` — *InputProductCountdown* — The product countdown. ``` input InputProductCountdown { enabled: Boolean! evergreen: Boolean! minutes: Int due: String } ```
- `sticky` — *InputProductSticky* — The product sticky. ``` input InputProductSticky { enabled: Boolean! } ```
- `faq` — *[InputProductFaq!]* — The product faq. ``` input InputProductFaq { id: String! question: String! answer: String! } ```
- `notice_text` — *String* — The product notice text.
- `product_type` — *ProductType* — The product type. ``` enum ProductType { physical_product digital_product } ```
- `shipping_group_id` — *String* — The product shipping group id.
- `price_bundle_id` — *String* — The product price bundle id.
- `file_id` — *ID* — The product file id.
- `crossSellProducts` — *[CrossInputSellProduct!]* — The product enable price bundle option. ``` input CrossInputSellProduct { upsell_product_uid: ID! downsell_product_uid: ID } ```
- `enable_inventory_limit` — *Boolean* — The product file id.
- `inventory_quantity` — *Int* — The product file id.
- `custom_options` — The product custom options.
- `enable_custom_options` — *Boolean* — The product enable custom options boolean.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: InputProduct!) {
	createProduct(node: $node){
		# Product fields
	}
}

```

### InputUpdateProduct

#### Fields

- `title` — *String* — The product title.
- `sku` — *String* — The product sku.
- `slug` — *String* — The product slug.
- `description` — *String* — The product description.
- `price` — *Float* — The product price.
- `compare_at_price` — *Float* — The product compare price.
- `options` — *[InputProductOption!]!* — The product options. ``` input InputProductOption { id: String label: String options: [String!] type: ProductOptionTypeEnum! = text options_types: [InputProductOptionType!]! = [] } input InputProductOptionType { option_id: String! value: ProductOptionTypeValue! } scalar ProductOptionTypeValue ```
- `images` — *[ID!]* — The product images.
- `variants` — *[InputProductVariant!]!* — The product variants.
- `tags` — *[ID!]* — The product tags.
- `order_bump` — *InputProductBump* — The product order bump. ``` input InputProductBump { id: String! title: String! price: Float! compare_at_price: Float! description: String! sku: String! enabled: Boolean! image_uid: ID file_uid: ID } ```
- `countdown` — *InputProductCountdown* — The product countdown. ``` input InputProductCountdown { enabled: Boolean! evergreen: Boolean! minutes: Int due: String } ```
- `sticky` — *InputProductSticky* — The product sticky. ``` input InputProductSticky { enabled: Boolean! } ```
- `features` — *[InputProductFeatures!]* — The product features. ``` input InputProductFeatures { id: String! title: String! description: String! image_uid: ID } ```
- `testimonials` — *[InputProductTestimonials!]* — The product testimonials. ``` input InputProductTestimonials { id: String! name: String! position: String! comment: String! image_uid: ID } ```
- `faq` — *[InputProductFaq!]* — The product faq. ``` input InputProductFaq { id: String! question: String! answer: String! } ```
- `notice_text` — *String* — The product notice text.
- `product_type` — *ProductType* — The product type. ``` enum ProductType { physical_product digital_product } ```
- `file_uid` — *ID* — The product file uid.
- `shipping_group_id` — *String* — The product shipping group id.
- `price_bundle_id` — *String* — The product price bundle id.
- `crossSellProducts` — *[CrossInputSellProduct!]* — The product cross-sell products option. ``` input CrossInputSellProduct { upsell_product_uid: ID! downsell_product_uid: ID } ```
- `custom_funnel_uid` — *String* — The product custom funnel id.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation updateProductMutation($node: InputUpdateProduct!, $id: Int!){
	updateProduct(node: $node, id: $id){
		# Product fields
	}
}

```

---

### ProductVariant

#### Fields

- `id` — *ID!* — Unique identifier for the product.
- `_id` — *Float!* — Unique number identifier for the product.
- `price` — *Float!* — The product price.
- `compare_at_price` — *Float!* — The product compare price.
- `sku` — *String!* — The product sku.
- `title` — *String!* — The product title.
- `image` — The product image.
- `image_id` — *ID* — The product image id.
- `file` — The product file.
- `file_id` — *ID* — The product file id.
- `product_id` — *ID!* — The product id.
- `product_id` — *ID!* — The product id.
- `product` — Resolves the parent product associated with this variant. Use this property to access details of the main product, such as its name, category, tags or shared attributes. This is particularly useful when working with product variants and needing context about their parent product.
- `options` — *[ProductOptionValue!]!* — The product options. ``` type ProductOptionValue { id: String! value: String! } ```
- `labeldOptions` — *[OrderVariantOption!]!* — The product options. ``` type OrderVariantOption { id: String! label: String! value: String! } ```
- `enable_inventory_limit` — *Boolean!* — The product enable inventory limit boolean.
- `inventory_quantity` — *Int!* — The product inventory quantity.
- `updated_at` — Timestamp of when the product was updated.
- `created_at` — Timestamp of when the product was created.

---

### File

#### Fields

- `id` — *ID!* — Unique identifier for the product file.
- `uid` — *ID!* — Unique identifier for the product file.
- `_id` — *Int!* — Unique number identifier for the product file.
- `updated_at` — Timestamp of when the product file was updated.
- `created_at` — Timestamp of when the product file was created.
- `title` — *String!* — The product file title.
- `path` — *String!* — The product file path.
- `key` — *String!* — The product file key.
- `format` — String — The size format string.

---

### Tag

#### Fields

- `id` — *ID!* — Unique identifier for the product tag.
- `uid` — *ID!* — Unique identifier for the product tag.
- `title` — *String!* — The product tag title.
- `updated_at` — Timestamp of when the product tag was updated.
- `created_at` — Timestamp of when the product tag was created.

---

### ProductConnection

#### Fields

- `pageInfo` — *PageInfo!* — Product connection page info. ``` type PageInfo { hasNextPage: Boolean! hasPreviousPage: Boolean! startCursor: String endCursor: String } ```
- `edges` — *[ProductEdge]* — The Product connection edges. ``` type ProductEdge { node: Product cursor: String! } ```
- `count` — *Int!* — Product connection count.

---

### CustomOption

#### Fields

- `id` — *ID!* — Unique identifier for the product custom option.
- `type` — *CustomOptionType!* — Product custom option type. ``` enum CustomOptionType { image text } ```
- `name` — *String!* — Product custom option name.
- `placeholder` — *String!* — Product custom option placeholder.

---

### CustomOptionInput

#### Fields

- `id` — *ID!* — Unique identifier for the product custom option.
- `type` — *CustomOptionType!* — Product custom option type. ``` enum CustomOptionType { image text } ```
- `name` — *String!* — Product custom option name.
- `placeholder` — *String!* — Product custom option placeholder.

---

### ProductBump

#### Fields

- `id` — *String!* — Unique identifier for the product bump.
- `title` — *String!* — Product bump title.
- `price` — *Float!* — Product bump price.
- `compare_at_price` — *Float!* — Product bump compare at price.
- `description` — *String!* — Product bump description.
- `enabled` — *Boolean!* — Product bump enabled.
- `image` — *Image* — Product bump image.
- `image_id` — *ID* — Product bump image id.
- `file_id` — *ID* — Product bump file id.
- `sku` — *String!* — Product bump sku.
- `file` — Product bump file.

---

### ProductFeatures

#### Fields

- `id` — *String!* — Unique identifier for the product features.
- `title` — *String!* — Product features title.
- `description` — *String!* — Product features description.
- `image` — Product features image.
- `image_id` — *ID* — Product features image id.

---

### ProductTestimonials

#### Fields

- `image` — Product testimonials image.
- `image_id` — *ID* — Product testimonials description.
- `id` — *String!* — Unique identifier for the product testimonials.
- `name` — *String!* — Product testimonials name.
- `position` — *String!* — Product testimonials position.
- `comment` — *String!* — Product testimonials comment.

---

### CrossSellProduct

#### Fields

- `upsell_product_id` — *ID!* — Unique identifier for the product upsell.
- `upsell_product` — Product upsell.
- `downsell_product_id` — *ID* — Downsell product id.
- `downsell_product` — Product downsell.

---

### InputProductOption

#### Fields

- `id` — *String* — Unique identifier for the product option.
- `label` — *String* — The product label.
- `options` — *[String!]* — The product options.
- `type` — *ProductOptionTypeEnum!* — The product title. ``` enum ProductOptionTypeEnum { image text color } ```
- `options_types` — *[ProductOptionType!]!* — The product options types. ``` type InputProductOptionType { option_id: String! value: ProductOptionTypeValue! } scalar ProductOptionTypeValue ```

---

### InputProductVariant

#### Fields

- `id` — *ID!* — Unique identifier for the product.
- `price` — *Float* — The product price.
- `compare_at_price` — *Float* — The product compare price.
- `image_id` — *ID* — The product image id.
- `file_id` — *ID* — The product file id.
- `sku` — *String* — The product sku.
- `options` — *[InputProductOptionValue!]!* — The product options. ``` input InputProductOptionValue { value: String! id: String! } ```
- `enable_inventory_limit` — *Boolean* — The product enable inventory limit boolean.
- `inventory_quantity` — *Int* — The product inventory quantity.

---

### InputProductBump

#### Fields

- `id` — *String!* — Unique identifier for the product bump.
- `title` — *String!* — Product bump title.
- `price` — *Float!* — Product bump price.
- `compare_at_price` — *Float!* — Product bump compare at price.
- `description` — *String!* — Product bump description.
- `sku` — *String!* — Product bump sku.
- `enabled` — *Boolean!* — Product bump enabled.
- `image_id` — *ID* — Product bump image id.
- `file_id` — *ID* — Product bump file id.

---

## Bundles Types

This list contains all query and inputs types for the bundle endpoints.

---

### PriceBundle

#### Fields

- `id` — *ID!* — Unique identifier for the price bundle.
- `updated_at` — Timestamp of when the price bundle was updated.
- `created_at` — Timestamp of when the price bundle was created.
- `label` — *String!* — The price bundle label.
- `items` — The price bundle items.
- `products` — The price bundle products.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query BundlesQuery($first: Int, $after: String, $query: String!){
	priceBundles(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				label
				created_at
				items {
					id
					discount_value
					quantity
					...
				}
				...
			}
		}
	}
}

```

---

### InputPriceBundle

#### Fields

- `label` — *String!* — The price bundle label.
- `items` — The price bundle items.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: InputPriceBundle!) {
	createPriceBundle(node: $node){
		# PriceBundle fields
	}
}

```

---

### InputUpdatePriceBundle

#### Fields

- `label` — *String!* — The price bundle label.
- `items` — The price bundle items.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation updateBundleMutation($node: InputUpdatePriceBundle!, $id: ID!){
	updatePriceBundle(node: $node, id: $id){
		# PriceBundle fields
	}
}

```

---

### PriceBundleItem

#### Fields

- `id` — *ID!* — Unique identifier for the price bundle item.
- `label` — *String!* — The price bundle label.
- `sticker_text` — *String* — The price bundle sticker text.
- `offer_text` — *String* — The price bundle offer text.
- `quantity` — *Int!* — The price bundle quantity.
- `discount_value` — *Float!* — The price bundle label.
- `discount_type` — *AllDiscountType!* — The price bundle label.

```
enum AllDiscountType {
	percentage
	fixed
	item
}

```

---

### InputPriceBundleItem

#### Fields

- `id` — *ID!* — Unique identifier for the price bundle item.
- `label` — *String!* — The price bundle label.
- `quantity` — *Int!* — The price bundle quantity.
- `discount_value` — *Float!* — The price bundle label.
- `discount_type` — *AllDiscountType!* — The price bundle label.

```
enum AllDiscountType {
	percentage
	fixed
	item
}

```

---

### PriceBundleConnection

#### Fields

- `pageInfo` — *PageInfo!* — Price bundle connection page info. ``` type PageInfo { hasNextPage: Boolean! hasPreviousPage: Boolean! startCursor: String endCursor: String } ```
- `edges` — *[PriceBundleEdge]* — The price bundle connection edges. ``` type PriceBundleEdge { node: PriceBundle cursor: String! } ```

---

### PriceBundleSnapshot

#### Fields

- `id` — *ID!* — Unique identifier for the priceBundle snapshot.
- `value` — *Float!* — The priceBundle snapshot value.
- `discount_result` — *Float!* — The priceBundle snapshot result.
- `label` — *String!* — The priceBundle snapshot label
- `type` — *AllDiscountType* — The priceBundle snapshot type. ``` enum AllDiscountType { percentage fixed item } ```
- `updated_at` — Timestamp of when the priceBundle snapshot was updated.
- `created_at` — Timestamp of when the priceBundle snapshot was created.

---

## Collections Types

This list contains all query and inputs types for the collection endpoints.

---

### Collection

#### Fields

- `id` — *ID!* — Unique identifier for the collection.
- `uid` — *ID!* — Unique identifier for the collection.
- `type` — *CollectionType!* — The collection type. ``` enum CollectionType { specific_funnels specific_keywords } ```
- `products_ids` — *[ID!]!* — The products unique identifiers for the collection.
- `tags_ids` — *[String!]!* — The tags unique identifiers for the collection.
- `name` — *String!* — The collection name.
- `slug` — *String!* — The collection slug.
- `image` — *Image* — The collection image.
- `image_id` — *ID* — The collection image unique identifier.
- `description` — *String!* — The collection description.
- `productsCount` — *Int!* — The collection products count.
- `result` — *[CollectionResult!]!* — The collection result. ``` Arguments cursor: String ```
- `updated_at` — Timestamp of when the collection was updated.
- `created_at` — Timestamp of when the collection was created.

---

### CollectionResult

#### Fields

- `title` — *String!* — The collection result title.
- `price` — *Float!* — The collection result price.
- `thumbnail` — *String* — The collection result thumbnail.
- `compare_at_price` — *Float!* — The collection result compare at price.
- `reviews_value` — *Float!* — The collection result reviews value.
- `link` — *String* — The collection result link.
- `slug` — *String!* — The collection result slug.
- `cursor` — *String!* — The collection result cursor.

---

### CollectionInput

#### Fields

- `type` — *CollectionType!* — The collection type. ``` enum CollectionType { specific_funnels specific_keywords } ```
- `tags_ids` — *[String!]* — The tags unique identifiers for the collection.
- `products_ids` — *[ID!]* — The products unique identifiers for the collection.
- `slug` — *String!* — The collection slug.
- `name` — *String!* — The collection name.
- `image_id` — *ID* — The collection image unique identifier.
- `description` — *String!* — The collection description.

---

### CollectionUpdateInput

#### Fields

- `type` — *CollectionType* — The collection type. ``` enum CollectionType { specific_funnels specific_keywords } ```
- `tags_ids` — *[String!]* — The tags unique identifiers for the collection.
- `products_ids` — *[ID!]* — The products unique identifiers for the collection.
- `slug` — *String* — The collection slug.
- `name` — *String* — The collection name.
- `image_id` — *ID* — The collection image unique identifier.
- `description` — *String* — The collection description.

---

### CollectionConnection

#### Fields

- `pageInfo` — *PageInfo!* — Collection connection page info. ``` type PageInfo { hasNextPage: Boolean! hasPreviousPage: Boolean! startCursor: String endCursor: String } ```
- `edges` — *[CollectionEdge]* — The Collection connection edges. ``` type CollectionEdge { node: Collection cursor: String! } ```

---

## Orders Types

This list contains all query and input types for the order endpoints.

---

### Order

#### Fields

- `id` — *ID!* — Unique identifier for the Order.
- `_id` — *Int!* — Unique number identifier for the Order.
- `account_id` — *ID!* — A unique number identifier representing the account that received the order.
- `updated_at` — Timestamp of when the order was updated.
- `created_at` — Timestamp of when the order was created.
- `archived_at` — Timestamp of when the order was archived.
- `cancelled_at` — Timestamp of when the order was cancelled.
- `email` — *Email!* — The email address associated with the customer. ``` scalar Email ```
- `phone` — *Phone!* — The phone number associated with the customer. ``` scalar Phone ```
- `name` — *String!* — A human-readable identifier for the order, typically formatted as a stringified number with a # prefix (e.g., #120).
- `notes` — *String* — Optional notes or comments associated with the order. This field can store additional information or instructions related to the order, such as special requests from the customer or internal notes for order handling.
- `financial_status` — *OrderFinancialStatus!* — The current financial status of the order. This field indicates the payment state of the order and is represented by the OrderFinancialStatus enum. Possible values include: ``` enum OrderFinancialStatus { pending paid refunded partially_refunded } ```
- `fulfillment_status` — *OrderFulfillmentStatus!* — The current fulfillment status of the order, indicating how much of the order has been fulfilled or shipped. This field is represented by the OrderFulfillmentStatus enum, with the following possible values: ``` enum OrderFulfillmentStatus { unfulfilled fulfilled partial } ```
- `client_details` — *ClientDetails!* — Information about the customer's client (device and browser) used to place the order. This field is represented by the ClientDetails type, which includes the following properties: ``` type ClientDetails { ip: String! device: String user_agent: String } ```
- `custom` — *CustomFields!* — A set of custom fields associated with the order. These fields allow for the storage of additional, order-specific data beyond the predefined fields in the API. The CustomFields scalar type represents a flexible structure, which can hold custom key-value pairs or other metadata relevant to the order. ``` scalar CustomFields ```
- `tags` — *[String!]!* — A list of tags associated with the order. Tags are used to categorize or label orders for easier filtering and organization. Each tag is a non-null string, and the list itself cannot be empty.
- `discount_value` — *Float!* — The total monetary value of discounts applied to the order. This value represents the amount subtracted from the original order total due to bundle discounts, coupon codes, or other discount mechanisms. The discount is expressed as a floating-point number, typically in the order’s currency.
- `bundle_discount_value` — *Float!* — The total monetary value of discounts specifically applied to bundled products within the order. This value reflects the discount provided when multiple products are purchased together as part of a bundle promotion. It is expressed as a floating-point number, typically in the currency of the order.
- `normal_discount_value` — *Float!* — The total monetary value of standard discounts applied to the order, typically through the use of coupon codes. This value represents the coupon code discount amount subtracted from the order total and is expressed as a floating-point number, usually in the currency of the order.
- `total` — *Float!* — The final total cost of the order, after applying all discounts, taxes, and shipping fees. This value represents the amount the customer is required to pay and is expressed as a floating-point number in the currency of the order.
- `shipping` — *Float!* — The total cost of shipping for the order. This value represents the amount charged for delivering the products to the customer, expressed as a floating-point number in the currency of the order. It includes any applicable shipping fees based on the chosen shipping method.
- `subtotal` — *Float!* — The subtotal cost of the order, representing the total price of all items before applying any discounts, taxes, or shipping fees. This value is expressed as a floating-point number in the currency of the order.
- `payments` — A list of payments associated with the order. An order can have multiple payments, such as the initial payment and additional payments for upsells or post-purchase modifications. Each payment is represented by the Payment object, detailing the amount, method, and other relevant payment information.
- `refunded_amount` — *Float!* — The total monetary amount that has been refunded for the order. This value represents the portion of the order's total that has been returned to the customer, whether through full or partial refunds, and is expressed as a floating-point number in the order's currency.
- `refundable` — *Float!* — The total amount of the order that is still eligible for a refund. This value is calculated as the difference between the total payment amount and the refunded amount. It is expressed as a floating-point number in the order's currency.
- `net_payment` — *Float!* — The net payment amount for the order, calculated as the total payment received minus any refunded amounts. This value represents the final amount the merchant retains after processing refunds, expressed as a floating-point number in the order's currency.
- `paid_by_customer` — *Float!* — The total amount of money paid by the customer for the order. This value includes any payments made for the order, including the initial payment and any additional payments, such as for upsells or shipping costs. It is expressed as a floating-point number in the currency of the order.
- `original_total` — *Float!* — The original total cost of the order before any discounts, refunds, or adjustments are applied. This value represents the full amount of the order as initially calculated, including all items, taxes, and shipping fees, and is expressed as a floating-point number in the currency of the order.
- `shipping_address` — The shipping address provided by the customer for the order. This address specifies where the order will be delivered and includes details such as the recipient's name, street address, city, state or region, postal code, and country.
- `billing_address` — The billing address associated with the customer’s payment method. This address is used for invoicing and payment verification purposes and typically includes details such as the customer’s name, street address, city, state or region, postal code, and country.
- `customer` — The details of the customer who placed the order. This field contains information such as the customer’s name, contact information (email, phone) etc.
- `customer_full_name` — *String* — The full name of the customer who placed the order, typically including both first and last names. This value is used for identification and communication purposes in order processing and customer service interactions.
- `items` — A list of items included in the order, represented as a union of either ProductVariantSnapshot or OrderBumpSnapshot. Each item in this list can be a product variant selected by the customer or an order bump item. This structure allows flexibility in representing different types of items within a single order.
- `checkout` — Details related to the order's checkout process. The Checkout object provides a snapshot of the final steps the customer took to complete the purchase.
- `test` — *Boolean!* — A flag indicating whether the order is a test transaction. If set to true, the order is considered a test and does not represent a real transaction. This is typically used for testing and development purposes to simulate order creation without processing actual payments.
- `nextOrderID` — *ID* — The unique identifier for the next sequential order related to this transaction. This field can be used to track or reference follow-up orders. If there is no subsequent order, this field may be null.
- `prevOrderID` — *ID* — The unique identifier of the previous order related to this transaction. This field can be used to reference any prior order in a sequence. If this is the first order, this field will be null.
- `link` — *String* — The URL link to the order's thank-you page. This page is typically displayed to the customer after the order has been successfully completed. The link provides a reference for the customer to review their order details and confirmation.
- `currency` — *String!* — The currency in which the order is priced and processed. This value is represented by a currency code following the ISO 4217 standard (e.g., "USD" for US Dollars, "EUR" for Euros). It defines the monetary unit for all prices, payments, and refunds associated with the order.
- `utm` — *[Utm!]* — A list of UTM (Urchin Tracking Module) parameters associated with the order, used for tracking the source of traffic or marketing campaigns that led to the purchase. Each Utm object contains the following fields: ``` type Utm { v: String! k: String! id: String! } ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query ordersQuery($first: Int, $after: String, $query: String!){
	orders(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				_id
				name
				total
				fulfillment_status
				financial_status
				customer {
					id
					full_name
				}
				...
			}
		}
	}
}

```

---

### InputOrder

#### Fields

- `notes` — *String* — Optional notes or comments to be attached to the order. This field allows users to provide additional information, special instructions, or internal comments when creating or updating an order. The content is flexible and can be used for various purposes, such as customer preferences or handling instructions.
- `archived` — *Boolean* — A flag indicating whether the order should be marked as archived. When set to true, the order is moved to an archived state, typically used for organizing or filtering completed or inactive orders.
- `shipping_address` — The customer’s shipping address. This field includes the full details required for order delivery, such as the recipient’s name, street address, city, state or region, postal code, and country. The address is essential for shipping and fulfillment purposes.
- `billing_address` — The billing address associated with the customer's payment method. This address is used for payment processing and verification, and should include full details such as the customer’s name, street address, city, state or region, postal code, and country.
- `email` — *String* — The email address of the customer placing the order. It must be a valid email format, ensuring successful delivery of important order information.
- `phone` — *String* — The customer's phone number, used for contact regarding the order. It should be provided in a valid format, including the appropriate country code if applicable.
- `sync_customer_details` — *Boolean* — A flag indicating whether to synchronize and override the customer details with updated information. When set to true, the existing customer information on the order will be replaced with the latest details provided.
- `items` — *[ID!]* — A list of IDs representing the items included in the order. Each ID can refer to a product variant or an order bump, allowing flexibility in what can be included in the order. This field is required when updating an order, and it supports both regular items and upsell (order bump) items.
- `variants` — *[Int!]* — A list of variant number ids associated with the products in the order. This field is used to specify which product variants the customer has selected as part of the order.
- `custom` — *CustomFields* — Custom fields associated with the order, allowing the storage of additional, user-defined data beyond the predefined fields. The CustomFields scalar type is flexible and can hold custom key-value pairs or other metadata relevant to the order, providing room for extra information based on business needs. ``` scalar CustomFields ```
- `tags` — *[String!]* — A list of tags associated with the order. Tags are used to categorize or label orders for easier filtering, organization, or tracking. Each tag is a non-null string.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation updateOrderMutation($node: InputOrder!, $id: Int!){
	updateOrder(node: $node, id: $id){
		# Order type fields
	}
}

```

---

### Payment

#### Fields

- `id` — *ID!* — Unique identifier for the payment.
- `_id` — *Int!* — Unique number identifier for the payment.
- `updated_at` — Timestamp of when the payment was updated.
- `created_at` — Timestamp of when the payment was created.
- `discount_snapshot` — A snapshot of the discount applied to the payment at the time of transaction. This includes details of the promotional code, discount type etc.
- `price_bundle_snapshot` — A list of snapshots representing bundled pricing and discounts applied to the payment at the time of the transaction. Each snapshot captures the details of a pricing bundle, such as the applied discount, bundle value, and type of discount used. This field provides a historical record of the price bundle at the time of payment.
- `total` — *Float!* — The total amount paid for the order, including any applied discounts, and shipping fees. This value represents the final sum charged to the customer for the transaction and is expressed as a floating-point number in the currency of the order.
- `sub_total` — *Float!* — The subtotal amount for the payment, representing the total cost of the items before any discounts, or shipping fees are applied. This value reflects the base price of the order and is expressed as a floating-point number in the currency of the order.
- `refunds` — *[Refund]* — A list of refunds associated with the payment. Each refund represents a partial or full return of funds to the customer for this transaction. This field provides details on all refund actions taken for the payment. ``` type Refund { id: ID! _id: Int! amount: Float! reason: String } ```
- `refunded` — *Float!* — The total amount that has been refunded for the payment. This value represents the sum of all refunds issued for the transaction, expressed as a floating-point number in the currency of the order. It reflects the portion of the payment returned to the customer.
- `refundable` — *Float!* — The total amount of the payment that is still eligible for a refund. This value is calculated as the difference between the total payment amount and the refunded amount. It is expressed as a floating-point number in the order's currency.
- `paid` — *Float!* — The total amount successfully paid by the customer for the transaction. This value represents the actual funds received, excluding any refunds, and is expressed as a floating-point number in the currency of the order.
- `paid_at` — The timestamp when the payment was successfully made.
- `discount_value` — *Float!* — The total monetary value of discounts applied to the payment. This includes all promotions, coupon codes, or special offers that reduced the overall amount paid by the customer. The discount is expressed as a floating-point number in the currency of the order.
- `source` — The source of the payment, providing details about how the payment was processed and through which system. The Source type contains information such as the order, payment gateway, and relevant timestamps for tracking the source of the payment.
- `shipping` — *Shipping* — Information about the shipping details associated with the payment, including the shipping cost, any applicable discounts, and the shipping label. This field provides an overview of how the order’s shipping was handled as part of the payment process. ``` type Shipping { id: ID! _id: Int! price: Float! discount_value: Float! label: String! } ```
- `paymentMethodLabel` — *String!* — A label describing the payment method used for the transaction. This provides a user-friendly name for the payment method, such as "Stripe," or "PayPal," helping to identify how the payment was processed.
- `financial_status` — *VariantSnapshotFinancialStatus* — The financial status of the payment, indicating the current state of the transaction. The status is represented by the VariantSnapshotFinancialStatus enum, with the following possible values: ``` enum VariantSnapshotFinancialStatus { pending paid } ```
- `items` — A list of items associated with the payment, represented as a union of either ProductVariantSnapshot or OrderBumpSnapshot. Each item reflects a product variant or an order bump that was part of the transaction paid for.
- `external_payment` — Represents details of an external payment processed through third-party payment gateways such as Tap, Razorpay, or others. This field is included for payments that were completed using external systems rather than native methods.
- `cookies` — *Scalar* — Here you get the cookies that you've set on the storefront using cookies prefix of your app(you can specify it on our Partners platform, in app configuration). When requesting this field, we return cookies that start with your cookies prefix followed by an underscore, `eg: otalp_1`. To see a concrete response schema, you can check orders/payments webhooks payload.

---

### ProductVariantSnapshotOrOrderBumpSnapshot

ProductVariantSnapshotOrOrderBumpSnapshot type can be either
- [`VariantSnapshot`](https://developer.lightfunnels.com/orders/types#variant-snapshot)

or
- [`OrderBumpSnapshot`](https://developer.lightfunnels.com/orders/types#order-bump-snapshot)

```
union ProductVariantSnapshotOrOrderBumpSnapshot = VariantSnapshot | OrderBumpSnapshot

```

---

### ExternalPayment

#### Fields

- `id` — *String* — The unique identifier assigned to the payment by the external gateway. Useful for tracking and reconciling transactions between your platform and the external payment provider.

---

### DiscountSnapshot

#### Fields

- `id` — *ID!* — Unique identifier for the discount snapshot.
- `_id` — *Int!* — Unique number identifier for the discount snapshot.
- `code` — *String* — The discount code applied at the time of the transaction. This code represents a specific promotional offer or coupon that was used to reduce the total payment amount. It may be a string of characters or numbers that the customer entered during checkout to receive the discount.
- `value` — *Float* — The exact value of the discount associated with the discount code. This value can represent either a fixed amount or a percentage, depending on the type of discount applied. It reflects the user-defined discount that reduces the total payment amount.
- `discount_result` — *Float* — The actual discount amount applied to the payment, calculated based on the discount type. For example, if the discount is a percentage, this field returns the computed value after applying the percentage to the order total.
- `type` — *DiscountType* — The type of discount applied, indicating whether the discount is a fixed amount or a percentage of the total. The DiscountType enum has two possible values: ``` enum DiscountType { percentage fixed } ```
- `updated_at` — Timestamp of when the discount snapshot was updated.
- `created_at` — Timestamp of when the discount snapshot was created.

---

### Source

#### Fields

- `id` — *ID!* — Unique identifier for the payment source.
- `_id` — *String!* — Unique number identifier for the payment source.
- `order` — The order associated with this payment source. This field links the payment source to the corresponding Order object, providing context on which order the payment was made for.
- `payment_gateway` — The payment gateway used to process the transaction. This field references the PaymentGateway object, detailing the specific service or platform (e.g., Stripe, PayPal) that facilitated the payment.
- `updated_at` — Timestamp of when the payment source was updated.
- `created_at` — Timestamp of when the payment source was created.

---

### VariantSnapshot

#### Fields

- `id` — *ID!* — Unique identifier for the variant snapshot.
- `groupID` — *String!* — A string that references the actual variant number ID in the format `VariantSnapshot:variant_id` (e.g., VariantSnapshot:1856).
- `_id` — *Int!* — Unique number identifier for the variant snapshot.
- `updated_at` — Timestamp of when the variant snapshot was updated.
- `created_at` — Timestamp of when the variant snapshot was created.
- `removed_at` — *TimeStamp* — Timestamp of when the variant snapshot was removed.
- `title` — *String!* — The title or name of the product variant at the time the snapshot was taken. This field captures the product’s title as it appeared during the transaction, ensuring consistency even if the product title changes later.
- `sku` — *String!* — The SKU (Stock Keeping Unit) of the product variant at the time the snapshot was taken. The sku is a unique identifier used for inventory management and tracking, preserving the specific SKU value during the transaction.
- `image` — The image of the product variant as it appeared at the time the snapshot was taken. This field stores the reference to the product image used during the transaction, ensuring that the visual representation of the variant is preserved, even if the product image changes later.
- `price` — *Float!* — The price of the product variant at the time the snapshot was taken. This field captures the exact price during the transaction, ensuring that the price remains consistent for historical records, even if the product price is updated later.
- `options` — *[OrderVariantOption!]!* — A list of options for the product variant at the time the snapshot was taken. Each option represents a specific configuration or customization of the variant, such as size or color. The structure is defined by the OrderVariantOption type, which includes: ``` type OrderVariantOption { id: String! label: String! value: String! } ```
- `tracking_number` — *String* — The tracking number associated with the shipment of the product variant at the time the snapshot was taken. This field captures the shipping tracking number if applicable, providing a reference for tracking the delivery of the variant.
- `tracking_link` — *String* — The URL link for tracking the shipment of the product variant. This field provides a direct link to the carrier's tracking page, allowing real-time updates on the delivery status of the variant at the time the snapshot was taken.
- `carrier` — *String* — The name of the shipping carrier responsible for delivering the product variant at the time the snapshot was taken. This field identifies the carrier (e.g., "FedEx," "UPS," "DHL") associated with the shipment, providing context for tracking and delivery.
- `payment_id` — *ID!* — The unique identifier for the payment associated with the product variant at the time the snapshot was taken. This field links the variant to the corresponding payment, allowing for tracking and reference of the transaction details.
- `refund_id` — *ID* — The unique identifier for the refund associated with the product variant, if applicable. This field links the variant to a specific refund transaction, allowing for tracking and reference of any refunds issued for the variant. It may be `null` if no refund is associated.
- `variant_id` — *ID* — The unique identifier for the product variant at the time the snapshot was taken. This field links the snapshot to the specific product variant, allowing for tracking and reference to the original variant, even if changes are made later.
- `fulfillment_status` — *VariantSnapshotItemFulfillmentStatus!* — The fulfillment status of the product variant at the time the snapshot was taken. This field indicates whether the variant has been fulfilled (shipped) or not. The `VariantSnapshotItemFulfillmentStatus` enum has the following values: ``` enum VariantSnapshotItemFulfillmentStatus { none fulfilled } ```
- `financial_status` — *VariantSnapshotFinancialStatus!* — The financial status of the product variant at the time the snapshot was taken. This field indicates the current payment status for the variant. The `VariantSnapshotFinancialStatus` enum has the following values: ``` enum VariantSnapshotFinancialStatus { pending paid } ```
- `variant` — A reference to the current ProductVariant object, if it still exists. This field links the snapshot to the active product variant, allowing developers to retrieve up-to-date details about the variant, even after the snapshot was taken. If the variant has been deleted or modified, the snapshot still retains historical data, but this reference will point to the actual variant in the system, if available.
- `payment` — A reference to the Payment object associated with the variant snapshot. This field links the variant to the specific payment made for it, allowing developers to retrieve details about the transaction, such as payment method, total amount, and any related refunds.
- `customer_files` — *[CustomerFileGroup!]!* — Variant snapshot customer files. ``` type CustomerFileGroup { name: String files: [CustomerFile!]! } type CustomerFile { path: String! key: String! } ```
- `custom_options` — *[VariantSnapshotCustomOption!]!* — Variant customer options. ``` type VariantSnapshotCustomOption { key: String! name: String! type: CustomOptionType! files: [VariantSnapshotCustomOptionFile!] value: VariantSnapshotCustomOptionValue! } type VariantSnapshotCustomOptionFile { url: String } scalar VariantSnapshotCustomOptionValue ```
- `file` — Variant snapshot file.

---

### OrderBumpSnapshot

#### Fields

- `id` — *ID!* — Unique identifier for the orderbump snapshot.
- `_id` — *Int!* — Unique number identifier for the orderbump snapshot.
- `groupID` — *String!* — A string that references the actual order bump group ID in the format `OrderBumpSnapshot:order_bump_id` (e.g., OrderBumpSnapshot:1234).
- `updated_at` — Timestamp of when the orderbump snapshot was updated.
- `created_at` — Timestamp of when the orderbump snapshot was created.
- `removed_at` — *TimeStamp* — Timestamp of when the orderbump snapshot was removed.
- `title` — *String!* — The title or name of the order bump product at the time the snapshot was taken. This field captures the product's title as it appeared during the transaction, ensuring that the name is preserved, even if the product title changes later.
- `sku` — *String!* — The SKU (Stock Keeping Unit) of the order bump product at the time the snapshot was taken. This unique identifier is used for tracking and inventory management, preserving the specific SKU used during the transaction, even if the product’s SKU changes later.
- `image` — The image of the order bump product at the time the snapshot was taken. This field stores the reference to the product image used during the transaction, preserving the visual representation of the order bump product even if the image is changed later.
- `price` — *Float!* — The price of the order bump product at the time the snapshot was taken. This field captures the exact price during the transaction, ensuring that the price is preserved for historical records, even if the product price is updated later.
- `tracking_number` — *String* — The tracking number associated with the shipment of the order bump product at the time the snapshot was taken. This field provides a reference for tracking the delivery of the order bump product, if applicable.
- `tracking_link` — *String* — The URL link for tracking the shipment of the order bump product. This field provides a direct link to the carrier’s tracking page.
- `carrier` — *String* — The name of the shipping carrier responsible for delivering the order bump product at the time the snapshot was taken. This field identifies the carrier (e.g., "FedEx," "UPS," "DHL"), providing context for shipment tracking and delivery.
- `payment_id` — *ID!* — The unique identifier for the payment associated with the order bump snapshot. This field links the order bump product to the corresponding payment, allowing for tracking and reference of the transaction details.
- `refund_id` — *ID* — The unique identifier for the refund associated with the order bump, if applicable. This field links the order bump product to a specific refund transaction, allowing for tracking and reference of any refunds issued. It may be null if no refund is associated with the order bump.
- `product_id` — *ID!* — The unique identifier for the actual product associated with the order bump. This field links to the current product in the system, allowing for tracking and reference of the active product, even after the snapshot was taken.
- `fulfillment_status` — *VariantSnapshotItemFulfillmentStatus* — The fulfillment status of the order bump product at the time the snapshot was taken. This field indicates whether the order bump product has been shipped or fulfilled. ``` enum VariantSnapshotItemFulfillmentStatus { none fulfilled } ```
- `financial_status` — *VariantSnapshotFinancialStatus!* — The financial status of the order bump product at the time the snapshot was taken. This field indicates the payment status for the order bump snapshot. ``` enum VariantSnapshotFinancialStatus { pending paid } ```
- `product` — A reference to the current Product object associated with the order bump. This field links the snapshot to the actual product in the system, allowing developers to retrieve up-to-date details about the product, even after the snapshot was taken.
- `payment` — A reference to the Payment object associated with the order bump snapshot. This field links the order bump product to the corresponding payment, allowing developers to track transaction details such as the payment method, total amount, and any associated refunds.
- `file` — Variant snapshot file.

---

### Checkout

#### Fields

- `id` — *ID!* — Unique identifier for the checkout.
- `_id` — *Int!* — Unique number identifier for the checkout.
- `updated_at` — Timestamp of when the checkout was updated.
- `created_at` — Timestamp of when the checkout was created.
- `customer` — *CheckoutCustomer!* — The customer information provided during the checkout process. This includes details such as the customer's name, contact information, and marketing preferences. ``` type CheckoutCustomer { first_name: String! last_name: String! full_name: String! email: Email! phone: Phone! accepts_marketing: Boolean! avatar: String! location: String! } ```
- `variants` — A list of product variants included in the checkout. Each item in the list is represented by the CheckoutVariant object, which contains details about the specific variant of product selected by the customer during the checkout process.
- `total` — *Float!* — The total cost of the checkout, including all products, shipping fees, and any applied discounts. This value represents the final amount the customer is required to pay and is expressed as a floating-point number in the currency of the checkout.
- `discount_value` — *Float!* — The total monetary value of standard discounts applied to the checkout, typically through the use of coupon codes. This value represents the coupon code discount amount subtracted from the checkout subtotal and is expressed as a floating-point number, usually in the currency of the checkout.
- `bundle_discount_value` — *Float!* — The total monetary value of discounts specifically applied to bundled products within the checkout. This value reflects the discount provided when multiple products are purchased together as part of a bundle promotion. It is expressed as a floating-point number, typically in the currency of the checkout.
- `subtotal` — *Float* — The subtotal amount of the checkout, representing the total cost of all items before applying discounts and shipping fees. This value is expressed as a floating-point number in the currency of the checkout.
- `email` — *String* — The email address provided by the customer during the checkout process. This email is used for sending order confirmations, receipts, and any other communications related to the order.
- `phone` — *String* — The phone number provided by the customer during the checkout process. This number may be used for order-related communication, such as shipping updates or customer service inquiries.
- `step` — The specific step or page in the checkout process where the checkout creation occurred.
- `link` — *String* — The URL of the checkout page, including the pre-filled checkout form. This link can be used to revisit the checkout page with all customer information and order details already entered.
- `store` — The store where the checkout was created. This field links to the Store object, providing information about the specific store associated with the checkout process.
- `funnel` — The funnel where the checkout was created. This field links to the Funnel object, providing information about the specific funnel associated with the checkout process.
- `currency` — *String!* — The currency in which the checkout is processed. This value is represented by a currency code (e.g., "USD" for US Dollars, "EUR" for Euros), determining the monetary unit for all prices, payments, and totals within the checkout.
- `recovered` — *Boolean* — A boolean flag indicating whether the checkout was successfully completed, meaning an order was created from this checkout. If `true`, it indicates the checkout resulted in a completed order; if `false`, no order was created from this checkout session.
- `shipping_address` — *CheckoutAddress* — Checkout shipping address. ``` type CheckoutAddress { first_name: String! last_name: String! full_name: String! email: Email! phone: Phone! accepts_marketing: Boolean! avatar: String! location: String! } ```
- `billing_address` — *CheckoutAddress* — Checkout billing address. ``` type CheckoutAddress { first_name: String! last_name: String! full_name: String! email: Email! phone: Phone! accepts_marketing: Boolean! avatar: String! location: String! } ```
- `utm` — *[Utm!]* — A list of UTM (Urchin Tracking Module) parameters associated with the order, used for tracking the source of traffic or marketing campaigns that led to the purchase. Each Utm object contains the following fields: ``` type Utm { v: String! k: String! id: String! } ```

---

### CheckoutVariant

#### Fields

- `variant` — A reference to the specific product variant included in the checkout. This field links the checkout variant to the corresponding ProductVariant object, allowing access to detailed information about the selected product variant
- `quantity` — *Int!* — The quantity of the product variant selected in the checkout. This field specifies how many units of the variant the customer has chosen to purchase during the checkout process.

---

### OrderConnection

#### Fields

- `pageInfo` — *PageInfo!* — Order connection page info. ``` type PageInfo { hasNextPage: Boolean! hasPreviousPage: Boolean! startCursor: String endCursor: String } ```
- `edges` — *[OrderEdge]* — The Order connection edges. ``` type OrderEdge { node: Order cursor: String! } ```

---

## Customers Types

This list contains all query and input types for the customer endpoints.

---

### Customer

#### Fields

- `id` — *ID!* — Unique identifier for the product.
- `_id` — *Int!* — Unique number identifier for the product.
- `updated_at` — Timestamp of when the product was updated.
- `created_at` — Timestamp of when the product was created.
- `email` — *Email!* — The customer email address.
- `phone` — *String!* — The customer phone number.
- `first_name` — *String!* — The customer first name.
- `last_name` — *String!* — The customer last name.
- `full_name` — *String!* — The customer full name.
- `location` — *String* — The customer location.
- `avatar` — *String!* — The customer avatar.
- `accepts_marketing` — *Boolean!* — The customer avatar.
- `notes` — *String* — The customer notes.
- `shipping_address` — The customer shipping address.
- `billing_address` — The customer billing address.
- `expenses` — *Float!* — The customer expenses.
- `orders_count` — *Int!* — The customer orders_count.
- `summary` — The customer summary.
- `custom` — *CustomFields* — The customer custom fields. ``` scalar CustomFields ```
- `leads` — *[Lead!]!* — The customer leads.
- `tags` — *[String!]!* — The customer tags.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query CustomersQuery($first: Int, $after: String, $query: String!){
	customers(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				email
				phone
				...
			}
		}
	}
}

```

---

### InputUpdateCustomer

#### Fields

- `email` — *String* — The customer email address.
- `phone` — *String* — The customer phone number.
- `first_name` — *String* — The customer first name.
- `last_name` — *String* — The customer last name.
- `accepts_marketing` — *Boolean* — Boolean to check if the customer accepts marketing.
- `notes` — *String* — The customer notes.
- `shipping_address` — The customer shipping address.
- `billing_address` — The customer billing address.
- `custom` — *CustomFields* — The customer custom fields. ``` scalar CustomFields ```
- `tags` — *[String!]* — The customer tags.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation updateCustomerMutation($node: InputUpdateCustomer!, $id: Int!){
	updateCustomer(node: $node, id: $id){
		# Customer type fields
	}
}

```

---

### InputCustomer

#### Fields

- `email` — *String!* — The customer email address.
- `phone` — *String!* — The customer phone number.
- `first_name` — *String!* — The customer first name.
- `last_name` — *String!* — The customer last name.
- `accepts_marketing` — *Boolean!* — Boolean to check if the customer accepts marketing.
- `shipping_address` — The customer shipping address.
- `billing_address` — The customer billing address.
- `tags` — *[String!]!* — The customer tags.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: InputCustomer!) {
	createCustomer(node: $node){
		# Customer type fields
	}
}

```

---

### InputAddress

#### Fields

- `line1` — *String* — The customer first address line.
- `line2` — *String* — The customer secondary address line.
- `city` — *String* — The customer city.
- `area` — *String* — The customer area.
- `country` — *String* — The customer country.
- `first_name` — *String* — The customer first name.
- `last_name` — *String* — The customer last name.
- `zip` — *String* — The customer zip.
- `state` — *String* — The customer state.
- `email` — *String* — The customer email address.
- `phone` — *String* — The customer phone number.

---

### Address

#### Fields

- `id` — *ID!* — Unique identifier for the customer.
- `_id` — *Int!* — Unique number identifier for the customer.
- `line1` — *String!* — The customer first address line.
- `line2` — *String!* — The customer secondary address line.
- `city` — *String!* — The customer city.
- `area` — *String!* — The customer area.
- `country` — *String* — The customer country.
- `first_name` — *String!* — The customer first name.
- `last_name` — *String!* — The customer last name.
- `zip` — *String!* — The customer zip.
- `state` — *String!* — The customer state.
- `email` — *String!* — The customer email address.
- `phone` — *String!* — The customer phone number.
- `toString` — *String!* — The toString field.

---

### CustomerSummary

#### Fields

- `visits` — *Int!* — The customer visits.
- `orders` — */customers/types#customer-orders* — The customer orders.

---

### CustomerOrders

#### Fields

- `expenses` — *Float!* — The customer expenses.
- `count` — *Int!* — The customer order count.
- `list` — */orders/types#order-summary* — The customer orders.

### OrderSummary

#### Fields

- `order` — The order type.
- `referrer` — *String* — The order referrer.

---

### CustomerConnection

#### Fields

- `pageInfo` — *PageInfo!* — Customer connection page info. ``` type PageInfo { hasNextPage: Boolean! hasPreviousPage: Boolean! startCursor: String endCursor: String } ```
- `edges` — *[CustomerEdge]* — The Customer connection edges. ``` type CustomerEdge { node: Customer cursor: String! } ```

---

## Discounts Types

This list contains all query and input types for the discount endpoints.

---

### Discount

#### Fields

- `id` — *ID!* — Unique identifier for the discount.
- `code` — *String!* — The discount code.
- `value` — *Float!* — The discount value.
- `type` — *DiscountType!* — The discount type. ``` enum DiscountType { percentage fixed } ```
- `usage_limit` — *Int!* — The discount usage limit.
- `one_time_usage_per_customer` — *Boolean!* — The discount one time usage per customer boolean.
- `active` — *Boolean!* — The discount active boolean.
- `limited_usage` — *Boolean!* — The discount limited usage boolean.
- `usage` — *Int* — The discount usage.
- `tags` — *[String!]!* — The discount tags.
- `product_ids` — *[ID!]!* — The discount product ids.
- `updated_at` — Timestamp of when the discount was updated.
- `created_at` — Timestamp of when the discount was created.
- `started_at` — Timestamp of when the discount will start.
- `expired_at` — Timestamp of when the discount will expire.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query DiscountsQuery($first: Int, $after: String, $query: String!){
	discounts(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				name
				description
				...
			}
		}
	}
}

```

---

### InputDiscount

#### Fields

- `code` — *String!* — The discount code.
- `value` — *Float!* — The discount value.
- `type` — *DiscountType!* — The discount type. ``` enum DiscountType { percentage fixed } ```
- `usage_limit` — *Int!* — The discount usage limit.
- `active` — *Boolean* — The discount active boolean.
- `one_time_usage_per_customer` — *Boolean!* — The discount one time usage per customer option.
- `limited_usage` — *Boolean!* — The discount limited usage option.
- `tags` — *[String!]* — The discount tags.
- `product_ids` — *[ID!]* — The discount product ids.
- `started_at` — *TimeStamp* — Timestamp of when the discount will start.
- `expired_at` — *TimeStamp* — Timestamp of when the discount will expire.

---

### InputUpdateDiscount

#### Fields

- `code` — *String* — The discount code.
- `value` — *Float* — The discount value.
- `type` — *DiscountType* — The discount type. ``` enum DiscountType { percentage fixed } ```
- `usage_limit` — *Int* — The discount usage limit.
- `active` — *Boolean* — The discount active option.
- `one_time_usage_per_customer` — *Boolean* — The discount one time usage per customer option.
- `limited_usage` — *Boolean* — The discount limited usage option.
- `tags` — *[String!]* — The discount tags.
- `product_ids` — *[ID!]* — The discount product ids.
- `started_at` — Timestamp of when the discount will start.
- `expired_at` — Timestamp of when the discount will expire.

---

### updateDiscountMutationInput

#### Fields

- `id` — *ID!* — Unique identifier for the discount.
- `node` — The discount node.
- `clientMutationId` — *String* — The discount client mutation id.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($input: updateDiscountMutationInput!) {
	updateDiscount(input: $input){
		# updateDiscountMutationPayload type fields
	}
}

```

---

### createDiscountMutationInput

#### Fields

- `node` — The discount node.
- `clientMutationId` — *String* — The discount client mutation id.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($input: createDiscountMutationInput!) {
	createDiscount(input: $input){
		# createDiscountMutationPayload type fields
	}
}

```

---

### updateDiscountMutationPayload

#### Fields

- `node` — The discount node.
- `clientMutationId` — *String* — The discount client mutation id.

---

### createDiscountMutationPayload

#### Fields

- `node` — The discount node.
- `clientMutationId` — *String* — The discount client mutation id.

---

### DiscountConnection

#### Fields

- `pageInfo` — *PageInfo!* — Discount connection page info. ``` type PageInfo { hasNextPage: Boolean! hasPreviousPage: Boolean! startCursor: String endCursor: String } ```
- `edges` — *[DiscountEdge]* — The Discount connection edges. ``` type DiscountEdge { node: Discount cursor: String! } ```

---

## Segments Types

This list contains all query and input types for the segment endpoints.

---

### Segment

#### Fields

- `id` — *ID!* — Unique identifier for the segment.
- `uid` — *ID!* — Unique identifier for the segment.
- `_id` — *Int!* — Unique numeral identifier for the segment.
- `settings` — *SegmentConfig!* — The segment settings. ``` type SegmentConfig { exclude: SegmentCondition! include: SegmentCondition! } type SegmentCondition { operator: SegmentConfigConditionType! tags: [String!]! } enum SegmentConfigConditionType { AND OR } ```
- `name` — *String!* — The segment name.
- `description` — *String!* — The segment description.
- `statistics` — *Int!* — The segment statistics.
- `updated_at` — Timestamp of when the segment was updated.
- `created_at` — Timestamp of when the segment was created.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
query SegmentsQuery($first: Int, $after: String, $query: String!){
	segments(query: "order_by:id order_dir:desc", after: "WzVE4OTA5LDEe/4OTA5XQ==", first: 10){
		edges{
			node{
				id
				name
				description
				...
			}
		}
	}
}

```

---

### SegmentInput

#### Fields

- `name` — *String* — The segment name.
- `description` — *String* — The segment description.
- `settings` — *InputSegmentConfig* — The segment settings. ``` input InputSegmentConfig { exclude: InputSegmentCondition include: InputSegmentCondition } input InputSegmentCondition { operator: SegmentConfigConditionType tags: [String!]! } enum SegmentConfigConditionType { AND OR } ```

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
mutation mutationName($node: SegmentInput!) {
	createSegment(node: $node){
		# Segment type fields
	}
}

```

---

### SegmentConnection

#### Fields

- `pageInfo` — *PageInfo!* — Segment connection page info. ``` type PageInfo { hasNextPage: Boolean! hasPreviousPage: Boolean! startCursor: String endCursor: String } ```
- `edges` — *[SegmentEdge]* — The Segment connection edges. ``` type SegmentEdge { node: Segment cursor: String! } ```

---

## Reviews Types

This list contains all query and inputs types for the review endpoints.

---

### Review

#### Fields

- `id` — *ID!* — Unique identifier for the review.
- `uid` — *ID!* — Unique identifier for the review.
- `created_at` — Timestamp of when the review was created.
- `updated_at` — Timestamp of when the review was updated.
- `content` — *String!* — The review content.
- `rate` — *Int!* — The review rate.
- `name` — *String!* — The review name.
- `email` — *String!* — The review email.
- `published` — *Boolean!* — The review published.
- `product_id` — *ID!* — The review product id.
- `avatar` — *String!* — The review avatar.
- `images` — The review images.
- `images_ids` — *[ID!]!* — The review image ids.
- `product` — The review product.
- `format` — String — the reviews format argument string defaults to "fromNow" (ImmutableJS) value.
- `suffix` — *Boolean* — the reviews suffix argument boolean defaults to true.

---

### InputReview

#### Fields

- `content` — *String!* — The review content.
- `rate` — *Int!* — The review rate.
- `name` — *String!* — The review name.
- `email` — *String* — The review email.
- `date` — The review date.
- `published` — *Boolean* — The review published.
- `images` — *[ID!]* — The review images.

---

### InputUpdateReview

#### Fields

- `content` — *String* — The review content.
- `rate` — *Int* — The review rate.
- `name` — *String* — The review name.
- `email` — *String* — The review email.
- `date` — *TimeStamp* — The review date.
- `published` — *Boolean* — The review published.
- `images` — *[ID!]* — The review images.

---

### ReviewConnection

#### Fields

- `pageInfo` — *PageInfo!* — Review connection page info. ``` type PageInfo { hasNextPage: Boolean! hasPreviousPage: Boolean! startCursor: String endCursor: String } ```
- `edges` — *[ReviewEdge]* — The Review connection edges. ``` type ReviewEdge { node: Review cursor: String! } ```

---

## Settings Types

*The official `/settings/types` page currently returns a 404 on developer.lightfunnels.com. Refer to the field lists in the Settings resource section (Part 2) above.*

---

## Shipping Rate Groups Types

This list contains all query types for the shipping rate groups endpoints.

---

### ShippingRateGroup

#### Fields

- `id` — *ID!* — Unique identifier of type number for the shipping rate group.
- `uid` — *ID!* — Unique identifier of type string for the shipping rate group.
- `label` — *String!* — The shipping rate group name.
- `zones` — The shipping rate group zones are used to define shipping rates per country or countries.

---

### ShippingZone

#### Fields

- `id` — *String!* — The unique identifier of the shipping zone.
- `label` — *String!* — The shipping zone name.
- `countries` — *[Country!]!* — It represents one country or more codes that the zone will be operating on (if you want to enable the 'rest of the world' pass '*').
- `rates` — It represents the shipping rates to be associated with the zone.

---

### ShippingRate

#### Fields

- `id` — *ID!* — The unique identifier of the shipping rate.
- `label` — *String!* — The name of the shipping rate.
- `price` — *Float!* — The price of the shipping rate.

---

### InputShippingRateGroup

#### Fields

- `label` — *String!* — The name of the shipping rate group.
- `zones` — The zones of the shipping rate group.

### InputZone

#### Fields

- `id` — *ID!* — The unique identifier of the zone, make sure it is of type String.
- `label` — *String!* — The name of the shipping rate group zone.
- `countries` — *[Country!]!* — Where you should pass list of countries codes that the zone will be operating on (if you want to enable the 'rest of the world' pass '*').
- `rates` — It represents the shipping rates to be associated with the zone.

### InputShippingRate

#### Fields

- `id` — *ID!* — The unique identifier of the shipping rate.
- `label` — *String!* — The name of the shipping rate.
- `price` — *Float!* — The price of the shipping rate.

---

## App Charges Types

---

### AppCharges

#### Fields

- `list` — The app charges list.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	# Query
	query AppChargeQuery{
	appCharges{
		list {
			# AppCharge type fields
		}
	}
}

```

---

### AppCharge

#### Fields

- `id` — *ID!* — Unique identifier for the app charge.
- `price` — *Float!* — The app charge amount.
- `name` — *String!* — The app charge name (plan name).
- `return_url` — *String!* — The app charge return url.
- `trial` — *Int!* — The app charge trial days.
- `url` — *String!* — The app charge url.
- `started_at` — Timestamp of when the app charge initiated.
- `accepted_at` — Timestamp of when the app charge was accepted.
- `ended_at` — Timestamp of when the app charge ended.
- `recurring` — The app charge recurring type.
- `app_client_id` — *String!* — The app client id.
- `test` — *Boolean!* — App charge test boolean.

---

### AppChargeInput

- `price` — *Float!* — The app charge amount.
- `return_url` — *String!* — The app charge return url.
- `name` — *String!* — The app charge name (plan name).
- `recurring` — The app charge recurring type.
- `trial` — *Int!* — The app charge trial days.
- `plan_id` — *ID!* — The app plan id.
- `test` — *Boolean! = false* — App charge test boolean.

---

### createAppChargeInput

#### Fields

- `node` — The app charge object node.

#### Request
**POST** `https://services.lightfunnels.com/api/v2`

```
	# Mutation
	mutation createAppChargeMutation($input: createAppChargeInput!) {
		createAppCharge(input: $input) {
			createAppChargePayload type fields
		}
	}

```

---

### createAppChargePayload

#### Fields

- `appCharge` — The app charge type.

---

### AppChargeInterval

- `AppChargeInterval` — *enum* — The app charge interval (defaults to month).

---

## Other / Shared Types

Shared scalar, object, and connection types used across all endpoints (source page: [/other](https://developer.lightfunnels.com/other)).

---

### TimeStamp

#### Arguments

- `format` — *String* — The supported format parameters: `fromNow` `YYYY-MM-DD` `HH:mm:ss`
- `suffix` — *Boolean* — TimeStamp suffix, defaults to `true`

##### Return type

- `scalar TimeStamp` ##### Example: ``` { updated_at('YYYY-MM-DD') --- updated_at: "2023-09-22" } ```

---

### Image

#### Fields

- `id` — *ID!* — The image unique identifier.
- `_id` — *Int!* — The image unique number identifier.
- `uid` — *ID!* — The image unique identifier.
- `title` — *String!* — The image title.
- `version` — ImageVariant — The image variant version. ``` enum ImageVariant { version1 version2 version3 } ```
- `key` — *String!* — The image key.
- `alt` — *String!* — The image alt.
- `resource_type` — *String!* — The image resource type.
- `overview` — The image resource type.
- `updated_at` — Timestamp of when the image was updated.
- `created_at` — Timestamp of when the image was created.

---

### ImageOverview

#### Fields

- `width` — *Float* — The image width.
- `height` — *Float* — The image height.
- `type` — *String* — The image type.
- `format` — String — format the image size type.

---

### Domain

#### Fields

- `id` — *ID!* — Unique identifier for the domain.
- `uid` — *ID!* — Unique identifier for the domain.
- `_id` — *Int!* — Unique numeral identifier for the domain.
- `name` — *String!* — The domain name.
- `connected` — *Boolean!* — The domain connected option.
- `ssl_connected` — *Boolean!* — The domain ssl connected option.
- `require_actions` — *Boolean!* — The domain require actions option.
- `redirect_to_primary` — *Boolean!* — The domain redirect to primary option.
- `registrar` — *String* — The domain registrar.
- `home_funnel` — */funnels/types#funnel* — The domain home funnel.
- `resource_type` — *FunnelResourceType* — The domain resource type. ``` enum FunnelResourceType { funnel store } ```
- `store_id` — *ID* — The domain store id.
- `updated_at` — Timestamp of when the domain was updated.
- `created_at` — Timestamp of when the domain was created.

---

### PaymentGateway

#### Fields

- `id` — *ID!* — Unique identifier for the payment gateway.
- `_id` — *Int!* — Unique numeral identifier for the payment gateway.
- `type` — *payment_gateway_type!* — The payment gateway type. ``` enum payment_gateway_type { paypal cod stripe external razorpay cinetpay thirdparty } ```
- `prototype` — the payment gateway prototype.
- `settings` — *PaymentGatewaySettings!* — The payment gateway settings. ``` scalar PaymentGatewaySettings ```
- `details` — *PaymentGatewayDetails!* — The payment gateway details. ``` scalar PaymentGatewayDetails ```
- `active` — *Boolean!* — The payment gateway active option.
- `identifier` — *String!* — The payment gateway identifier.
- `test` — *Boolean!* — The payment gateway test option.
- `platform_active` — *Boolean!* — The payment gateway platform active option.

---

### PaymentGatewayPrototype

- `id` — *ID!* — Unique identifier for the payment gateway prototype.
- `label` — *String!* — The payment gateway prototype label.
- `link` — *String!* — The payment gateway prototype link.
- `thumbnail` — *String!* — The payment gateway prototype thumbnail.
- `key` — *String!* — The payment gateway prototype key.
- `backendOnly` — *Boolean!* — The payment gateway prototype backendOnly boolean.
- `thirdparty` — *Boolean!* — The payment gateway prototype thirdparty boolean.
- `express` — *Boolean!* — The payment gateway prototype express boolean.
- `testMode` — *Boolean!* — The payment gateway prototype testMode boolean.
- `public` — *Boolean!* — The payment gateway prototype public boolean.
- `keys` — *PaymentGatewayPrototypeKeys!* — The payment gateway prototype keys. ``` scalar PaymentGatewayPrototypeKeys ```
- `connection_keys` — *PaymentGatewayPrototypeKeys!* — The payment gateway prototype connection keys. ``` scalar PaymentGatewayPrototypeKeys ```
---

# Field-Verified Addendum (not in official docs)

Findings from live testing against `https://services.lightfunnels.com/api/v2` on 2026-07-22 with an OAuth app token (scopes: funnels, products). These correct or extend the official documentation above.

## Page-content writes: blocked for APP tokens, allowed for SESSION tokens

The block is on the **credential type**, not the API:

**App tokens (OAuth, permanent):**
- `updateFunnel` **rejects** `steps`, `deleted_steps`, `styles`, `smart_sections` with error key `non_allowed_app_funnel_update` ("Apps are not allowed to update: steps, …").
- `createStep(funnel_id: ID!, node: InputStep!)` returns `Forbidden` / `errors_app_access_to_non_allowed_resources`.
- Writable: top-level funnel fields only — verified `name`, `slug`, `published`, `header_scripts`.

**Browser session tokens (from the LF dashboard, temporary):** NOT treated as an app, so the block does not apply. Verified working:
- `updateFunnel.steps` writes real page bodies (echo a captured body, or swap text inside it — changes persist and show in the LF editor). Requires headers `account-id: <id>` and `version: 1` plus a browser `Origin`/`Referer`.
- Non-destructive: `updateFunnel.steps` upserts steps by `id`; sending one step leaves siblings intact.
- `createStep` adds new pages successfully.
- A malformed `body` value yields a generic `UnknownError: Oops! Something went wrong` (not a permission error) — pass a real BuilderNode/StepBody structure.

Get a session token from DevTools → Network → any `services.lightfunnels.com/api/v2` request → `Authorization: bearer …` header (and the sibling `account-id` header). This is what AI page-builder apps (e.g. Pixelier) use: they operate on the user's login session, not an installed app. Session tokens expire; app tokens are permanent.

## createFunnel quirks

- `funnel_steps` is `[StepType!]!` (required, min 1 item) — but it does **not** create any steps. The created funnel has `steps: []`.
- `InputCreateFunnel` also accepts `steps: [CreateStepInput!]` (client-generated `id` `"step_<21-char nanoid>"` and `_id` int required) plus `references: [StepReference!]` — but every tested combination returns a server error (`UnknownError: Oops! Something went wrong`) on an app token. Treat step creation as unavailable to apps.

## Undocumented mutations that DO work for apps

- `duplicateFunnel(funnel_id: ID!): Funnel` — full server-side clone **including all pages/bodies**. Name gets ` [DUPLICATE]` appended, slug is regenerated, `published` state is inherited from the source.
- `importFunnel(code: String!): Funnel` — import from a funnel share code.
- `deleteFunnels(items: [ID!]!): [ID]` — works as documented.

## Introspection

- `__schema` queries are blocked ("GraphQL introspection is not allowed").
- `__type(name: "...")` queries **work** — use them to inspect any input/output type.
- Misspelled field errors return "Did you mean ..." suggestions, usable for mutation discovery.

## Practical notes

- Funnel/step `id` and `uid` are the same nanoid-style strings (`fun_...`, `step_...`); `_id` is the numeric counterpart.
- There is no singular `funnel(id:)` query; fetch one funnel via the `funnels` connection with `query: "id:fun_..."`. (The documented `node(id:)` interface query also exists.)
- Step `body` is opaque builder JSON; all human-visible rich text lives in `content` keys as HTML strings.
- Cloudflare fronts the API and 403s the default Python-urllib User-Agent — send a browser-like UA.
- Real step `settings` can legitimately be `{}`.
