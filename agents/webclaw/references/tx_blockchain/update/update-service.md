# Update Service

The Update Service is a special WebSocket-based service that publishes real-time updates to interested listeners. Unlike traditional services, it does not serve or accept requests for data directly. Instead, it listens on a PubSub topic and broadcasts messages to connected WebSocket clients.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Update Service Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│ │ Publisher │────▶│ PubSub │────▶│ Update Service │ │
│ │ Service │ │ Topic │ │ (Singleton) │ │
│ └──────────────┘ └──────────────┘ └────────────┬─────────────┘ │
│ │ │
│ ▼ │
│ ┌──────────────────────────────┐ │
│ │ WebSocket Connections │ │
│ │ wss://api/update/ws │ │
│ └──────────────┬───────────────┘ │
│ │ │
│ ▼ │
│ ┌──────────────────────────────┐ │
│ │ Connected Clients │ │
│ │ (Browser, Mobile, etc.) │ │
│ └──────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Message Types

### 1. System Style Messages
Messages without an identifying key. Used for global events that affect entire systems.

**Examples:**
- New AMM Pool created or removed
- System maintenance notification
- Global configuration changes

**Usage:** Clients should reload entire datasets to discover new data.

### 2. Entity Style Messages
Messages with an identifying key. Used for specific entity changes.

**Examples:**
- Token price changed
- Wallet balance updated
- Order status changed
- Trade executed

**Contains:** ID, type, and network for filtering

## Update Patterns

### Pattern 1: Event-Driven Updates (Trigger-based)

Delivers a message containing only an ID that clients must use to fetch complete data through additional API calls.
Client ──WebSocket──▶ Update Service ──▶ Receives Trigger
│
▼
Sends {ID: "xyz"}
│
▼
Client ──HTTP GET──▶ API Service ──▶ Fetches Full Data

text

**Use Cases:**
- Notifications
- KYC status updates
- Comment replies
- Support ticket updates

### Pattern 2: Time-Period Driven Updates

Delivers complete data objects at regular intervals through a polling mechanism.
Client ──WebSocket──▶ Update Service
│
▼
Every N seconds: Sends Complete Data Object
│
▼
Client receives full data (no additional API calls needed)

text

**Use Cases:**
- AED chart data
- Market prices
- Real-time balances

## WebSocket Connection

### Connection URL
wss://api.sologenic.org/api/v1/update/ws

text

### Initial Connection Response

Upon successful connection, the server responds:
Connected

text

### Keep-Alive Mechanism

Nginx has a timeout of approximately 10 seconds. To prevent disconnects, clients must send a keep-alive message every 5 seconds.

**Client sends:**
ping

text

**Server responds:**
pong {instanceID}

text

The `instanceID` is stable for the duration of the server instance. If the instance ID changes (due to crash or restart), clients should resubscribe to all topics.

## WebSocket Messages

### Message Structure

All messages are JSON objects with an `Action` field.

| Action | Value | Direction | Description |
|--------|-------|-----------|-------------|
| SUBSCRIBE | 0 | Client → Server | Subscribe to a topic |
| UNSUBSCRIBE | 1 | Client → Server | Unsubscribe from a topic |
| CLOSE | 2 | Client → Server | Close the connection |
| RESPONSE | 3 | Server → Client | Response message with update |

### Subscription Object

| Field | Type | Description |
|-------|------|-------------|
| Network | int | 1=mainnet, 2=testnet |
| OrganizationID | string | Organization UUID |
| Method | int | Update method enum value |
| ID | string | Entity identifier (for entity subscriptions) |

## Subscription Examples

### Subscribe to System Topic

```json
{
    "Action": 0,
    "Subscription": {
        "Network": 1,
        "OrganizationID": "024e6e3e-59e6-4037-be4d-bfbb3894dbeb",
        "Method": 3
    }
}
This subscribes to support ticket reply notifications.

Subscribe to Entity Topic
json
{
    "Action": 0,
    "Subscription": {
        "Network": 1,
        "OrganizationID": "024e6e3e-59e6-4037-be4d-bfbb3894dbeb",
        "Method": 2,
        "ID": "user_email@gmail.com"
    }
}
This subscribes to updates for a specific AMM pool.

Subscribe to Multiple Topics
json
{
    "Action": 0,
    "Subscription": [
        {
            "Network": 1,
            "OrganizationID": "024e6e3e-59e6-4037-be4d-bfbb3894dbeb",
            "Method": 2,
            "ID": "pool_123"
        },
        {
            "Network": 1,
            "OrganizationID": "024e6e3e-59e6-4037-be4d-bfbb3894dbeb",
            "Method": 3
        }
    ]
}
Unsubscribe
json
{
    "Action": 1,
    "Subscription": {
        "Network": 1,
        "OrganizationID": "024e6e3e-59e6-4037-be4d-bfbb3894dbeb",
        "Method": 3
    }
}
Close Connection
json
{
    "Action": 2
}
Note: Using the CLOSE action is preferred over simply disconnecting, as it allows the server to clean up subscriptions properly.

Server Response Messages
Response Structure
json
{
    "Action": 3,
    "Subscription": {
        "Network": 1,
        "Method": 2,
        "OrganizationID": "024e6e3e-59e6-4037-be4d-bfbb3894dbeb",
        "ID": "FOO_XRP_r123456"
    }
}
The ID field indicates which entity has changed and should be refreshed.

Update Methods (Enums)
Method	Value	Type	Description	ID Field
AMM_POOL	1	Entity	AMM pool changed	Pool ID
AMM_TRADE_FOR_ACCOUNT	2	Entity	Trade occurred for account	Account ID
SUPPORT_TICKET_REPLY	3	System	New reply on ticket	N/A
KYC_STATUS_CHANGE	4	Entity	KYC status updated	User ID
NOTIFICATION	5	Entity	New notification	Notification ID
BALANCE_UPDATE	6	Entity	Wallet balance changed	Wallet Address
ORDER_UPDATE	7	Entity	Order status changed	Order ID
TRADE_EXECUTION	8	Entity	Trade executed	Trade ID
PRICE_UPDATE	9	Entity	Token price changed	Token Denom
AED_DATA_REFRESH	10	System	AED chart data updated	N/A
COMMENT_REPLY	11	Entity	New comment reply	Comment ID
ASSET_UPDATE	12	Entity	Asset metadata changed	Asset Denom
Integration Examples
JavaScript/React Client
javascript
class UpdateServiceClient {
  constructor(url, organizationId, network = 1) {
    this.url = url;
    this.organizationId = organizationId;
    this.network = network;
    this.ws = null;
    this.subscriptions = new Map();
    this.listeners = new Map();
    this.pingInterval = null;
    this.instanceId = null;
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);
      
      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this._startKeepAlive();
        resolve();
      };
      
      this.ws.onmessage = (event) => {
        if (event.data === 'Connected') {
          console.log('Connected to update service');
        } else if (event.data.startsWith('pong')) {
          const newInstanceId = event.data.split(' ')[1];
          if (this.instanceId && this.instanceId !== newInstanceId) {
            console.warn('Instance ID changed, resubscribing...');
            this._resubscribeAll();
          }
          this.instanceId = newInstanceId;
        } else {
          this._handleMessage(JSON.parse(event.data));
        }
      };
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };
      
      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this._stopKeepAlive();
      };
    });
  }

  subscribe(method, id = null) {
    const subscription = {
      Action: 0, // SUBSCRIBE
      Subscription: {
        Network: this.network,
        OrganizationID: this.organizationId,
        Method: method
      }
    };
    
    if (id) {
      subscription.Subscription.ID = id;
    }
    
    const key = this._getSubscriptionKey(method, id);
    this.subscriptions.set(key, subscription);
    
    this._send(subscription);
  }

  unsubscribe(method, id = null) {
    const subscription = {
      Action: 1, // UNSUBSCRIBE
      Subscription: {
        Network: this.network,
        OrganizationID: this.organizationId,
        Method: method
      }
    };
    
    if (id) {
      subscription.Subscription.ID = id;
    }
    
    const key = this._getSubscriptionKey(method, id);
    this.subscriptions.delete(key);
    
    this._send(subscription);
  }

  on(method, callback) {
    if (!this.listeners.has(method)) {
      this.listeners.set(method, []);
    }
    this.listeners.get(method).push(callback);
  }

  off(method, callback) {
    if (this.listeners.has(method)) {
      const callbacks = this.listeners.get(method);
      const index = callbacks.indexOf(callback);
      if (index !== -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  disconnect() {
    this._send({ Action: 2 }); // CLOSE
    this._stopKeepAlive();
    if (this.ws) {
      this.ws.close();
    }
  }

  _send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  _handleMessage(message) {
    if (message.Action === 3) { // RESPONSE
      const method = message.Subscription.Method;
      const id = message.Subscription.ID;
      
      if (this.listeners.has(method)) {
        this.listeners.get(method).forEach(callback => {
          callback(id, message.Subscription);
        });
      }
      
      // Also trigger generic listener
      if (this.listeners.has('*')) {
        this.listeners.get('*').forEach(callback => {
          callback(method, id, message.Subscription);
        });
      }
    }
  }

  _startKeepAlive() {
    this.pingInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send('ping');
      }
    }, 5000);
  }

  _stopKeepAlive() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  _resubscribeAll() {
    for (const subscription of this.subscriptions.values()) {
      this._send(subscription);
    }
  }

  _getSubscriptionKey(method, id) {
    return id ? `${method}:${id}` : `${method}`;
  }
}

// React Hook Example
function useUpdateSubscription(method, id, onUpdate) {
  const [client] = useState(() => {
    return new UpdateServiceClient(
      'wss://api.sologenic.org/api/v1/update/ws',
      localStorage.getItem('orgId'),
      1 // mainnet
    );
  });

  useEffect(() => {
    client.connect().then(() => {
      client.on(method, onUpdate);
      client.subscribe(method, id);
    });

    return () => {
      client.unsubscribe(method, id);
      client.off(method, onUpdate);
    };
  }, [method, id]);

  return client;
}

// React Component Example
function AMMPoolMonitor({ poolId }) {
  const [poolData, setPoolData] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  const handlePoolUpdate = async (updatedPoolId) => {
    console.log(`Pool ${updatedPoolId} updated`);
    // Fetch fresh pool data
    const freshData = await fetchPoolData(updatedPoolId);
    setPoolData(freshData);
    setLastUpdate(new Date());
  };

  useUpdateSubscription(1, poolId, handlePoolUpdate); // Method 1 = AMM_POOL

  return (
    <div className="pool-monitor">
      <h3>AMM Pool Monitor</h3>
      {poolData && (
        <div>
          <p>Pool ID: {poolData.id}</p>
          <p>Balance: {poolData.balance}</p>
          <p>Last Update: {lastUpdate?.toLocaleTimeString()}</p>
        </div>
      )}
    </div>
  );
}

// Full Example: Wallet Balance Tracker
function WalletBalanceTracker({ walletAddress }) {
  const [balance, setBalance] = useState(null);
  const [notifications, setNotifications] = useState([]);

  const updateService = new UpdateServiceClient(
    'wss://api.sologenic.org/api/v1/update/ws',
    localStorage.getItem('orgId'),
    1
  );

  useEffect(() => {
    async function init() {
      await updateService.connect();
      
      // Subscribe to balance updates
      updateService.subscribe(6, walletAddress); // Method 6 = BALANCE_UPDATE
      
      // Subscribe to notifications
      updateService.subscribe(5); // Method 5 = NOTIFICATION
      
      // Handle balance updates
      updateService.on(6, async (address) => {
        if (address === walletAddress) {
          const newBalance = await fetchBalance(walletAddress);
          setBalance(newBalance);
          addNotification(`Balance updated: ${newBalance}`);
        }
      });
      
      // Handle notifications
      updateService.on(5, (notificationId) => {
        fetchNotification(notificationId).then(notification => {
          addNotification(notification.message);
        });
      });
    }
    
    init();
    
    return () => {
      updateService.unsubscribe(6, walletAddress);
      updateService.unsubscribe(5);
      updateService.disconnect();
    };
  }, [walletAddress]);
  
  function addNotification(message) {
    setNotifications(prev => [message, ...prev].slice(0, 10));
  }
  
  return (
    <div>
      <h3>Wallet Balance: {balance}</h3>
      <div className="notifications">
        <h4>Notifications</h4>
        <ul>
          {notifications.map((notif, i) => (
            <li key={i}>{notif}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export { UpdateServiceClient, useUpdateSubscription, AMMPoolMonitor, WalletBalanceTracker };
Python Client
python
import asyncio
import json
import websockets
from typing import Dict, List, Optional, Callable
from enum import IntEnum
import threading

class UpdateMethod(IntEnum):
    AMM_POOL = 1
    AMM_TRADE_FOR_ACCOUNT = 2
    SUPPORT_TICKET_REPLY = 3
    KYC_STATUS_CHANGE = 4
    NOTIFICATION = 5
    BALANCE_UPDATE = 6
    ORDER_UPDATE = 7
    TRADE_EXECUTION = 8
    PRICE_UPDATE = 9
    AED_DATA_REFRESH = 10
    COMMENT_REPLY = 11
    ASSET_UPDATE = 12

class Action(IntEnum):
    SUBSCRIBE = 0
    UNSUBSCRIBE = 1
    CLOSE = 2
    RESPONSE = 3

class UpdateServiceClient:
    def __init__(self, url: str, organization_id: str, network: int = 1):
        self.url = url
        self.organization_id = organization_id
        self.network = network
        self.websocket = None
        self.subscriptions = {}
        self.listeners = {}
        self.instance_id = None
        self._running = False
        self._ping_task = None
    
    async def connect(self):
        """Connect to the update service"""
        self.websocket = await websockets.connect(self.url)
        self._running = True
        
        # Wait for Connected message
        response = await self.websocket.recv()
        if response == "Connected":
            print("Connected to update service")
        
        # Start ping task
        self._ping_task = asyncio.create_task(self._keep_alive())
        
        # Start message handler
        asyncio.create_task(self._handle_messages())
    
    async def subscribe(self, method: UpdateMethod, entity_id: Optional[str] = None):
        """Subscribe to updates"""
        subscription = {
            "Action": Action.SUBSCRIBE,
            "Subscription": {
                "Network": self.network,
                "OrganizationID": self.organization_id,
                "Method": int(method)
            }
        }
        
        if entity_id:
            subscription["Subscription"]["ID"] = entity_id
        
        key = self._get_key(method, entity_id)
        self.subscriptions[key] = subscription
        
        await self.websocket.send(json.dumps(subscription))
    
    async def unsubscribe(self, method: UpdateMethod, entity_id: Optional[str] = None):
        """Unsubscribe from updates"""
        subscription = {
            "Action": Action.UNSUBSCRIBE,
            "Subscription": {
                "Network": self.network,
                "OrganizationID": self.organization_id,
                "Method": int(method)
            }
        }
        
        if entity_id:
            subscription["Subscription"]["ID"] = entity_id
        
        key = self._get_key(method, entity_id)
        if key in self.subscriptions:
            del self.subscriptions[key]
        
        await self.websocket.send(json.dumps(subscription))
    
    def on(self, method: UpdateMethod, callback: Callable):
        """Register a callback for updates"""
        if method not in self.listeners:
            self.listeners[method] = []
        self.listeners[method].append(callback)
    
    def off(self, method: UpdateMethod, callback: Callable):
        """Remove a callback"""
        if method in self.listeners:
            try:
                self.listeners[method].remove(callback)
            except ValueError:
                pass
    
    async def disconnect(self):
        """Disconnect from the service"""
        close_msg = {"Action": Action.CLOSE}
        await self.websocket.send(json.dumps(close_msg))
        self._running = False
        if self._ping_task:
            self._ping_task.cancel()
        await self.websocket.close()
    
    async def _keep_alive(self):
        """Send ping every 5 seconds"""
        while self._running:
            try:
                await asyncio.sleep(5)
                await self.websocket.send("ping")
            except Exception as e:
                print(f"Keep-alive error: {e}")
                break
    
    async def _handle_messages(self):
        """Handle incoming messages"""
        while self._running:
            try:
                message = await self.websocket.recv()
                
                if message.startswith("pong"):
                    parts = message.split()
                    if len(parts) > 1:
                        new_instance_id = parts[1]
                        if self.instance_id and self.instance_id != new_instance_id:
                            print("Instance ID changed, resubscribing...")
                            await self._resubscribe_all()
                        self.instance_id = new_instance_id
                else:
                    data = json.loads(message)
                    if data.get("Action") == Action.RESPONSE:
                        subscription = data.get("Subscription", {})
                        method = UpdateMethod(subscription.get("Method"))
                        entity_id = subscription.get("ID")
                        
                        if method in self.listeners:
                            for callback in self.listeners[method]:
                                await callback(entity_id, subscription)
                
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break
            except Exception as e:
                print(f"Error handling message: {e}")
    
    async def _resubscribe_all(self):
        """Resubscribe to all previously subscribed topics"""
        for subscription in self.subscriptions.values():
            await self.websocket.send(json.dumps(subscription))
    
    def _get_key(self, method: UpdateMethod, entity_id: Optional[str]) -> str:
        return f"{method.value}:{entity_id}" if entity_id else str(method.value)

# Usage Example
async def main():
    client = UpdateServiceClient(
        url="wss://api.sologenic.org/api/v1/update/ws",
        organization_id="024e6e3e-59e6-4037-be4d-bfbb3894dbeb",
        network=1
    )
    
    # Define callback for balance updates
    async def on_balance_update(entity_id, subscription):
        print(f"Balance updated for: {entity_id}")
        # Fetch fresh balance data
        # balance = await fetch_balance(entity_id)
        # print(f"New balance: {balance}")
    
    # Define callback for notifications
    async def on_notification(notification_id, subscription):
        print(f"New notification: {notification_id}")
        # Fetch notification details
        # notification = await fetch_notification(notification_id)
    
    # Register callbacks
    client.on(UpdateMethod.BALANCE_UPDATE, on_balance_update)
    client.on(UpdateMethod.NOTIFICATION, on_notification)
    
    # Connect and subscribe
    await client.connect()
    await client.subscribe(UpdateMethod.BALANCE_UPDATE, "r123456789")
    await client.subscribe(UpdateMethod.NOTIFICATION)
    
    # Keep running
    try:
        await asyncio.Future()  # run forever
    except KeyboardInterrupt:
        await client.disconnect()

# Run the client
# asyncio.run(main())
Go Client
go
package main

import (
    "encoding/json"
    "fmt"
    "sync"
    "time"
    
    "github.com/gorilla/websocket"
)

type Action int

const (
    ActionSubscribe   Action = 0
    ActionUnsubscribe Action = 1
    ActionClose       Action = 2
    ActionResponse    Action = 3
)

type UpdateMethod int

const (
    MethodAMMPool              UpdateMethod = 1
    MethodAMMTradeForAccount   UpdateMethod = 2
    MethodSupportTicketReply   UpdateMethod = 3
    MethodKYCStatusChange      UpdateMethod = 4
    MethodNotification         UpdateMethod = 5
    MethodBalanceUpdate        UpdateMethod = 6
    MethodOrderUpdate          UpdateMethod = 7
    MethodTradeExecution       UpdateMethod = 8
    MethodPriceUpdate          UpdateMethod = 9
    MethodAEDDataRefresh       UpdateMethod = 10
    MethodCommentReply         UpdateMethod = 11
    MethodAssetUpdate          UpdateMethod = 12
)

type Subscription struct {
    Network        int    `json:"Network"`
    OrganizationID string `json:"OrganizationID"`
    Method         int    `json:"Method"`
    ID             string `json:"ID,omitempty"`
}

type Message struct {
    Action       Action       `json:"Action"`
    Subscription *Subscription `json:"Subscription,omitempty"`
}

type UpdateServiceClient struct {
    url            string
    organizationID string
    network        int
    conn           *websocket.Conn
    mu             sync.RWMutex
    subscriptions  map[string]*Subscription
    listeners      map[UpdateMethod][]func(string, *Subscription)
    instanceID     string
    done           chan struct{}
}

func NewUpdateServiceClient(url, organizationID string, network int) *UpdateServiceClient {
    return &UpdateServiceClient{
        url:            url,
        organizationID: organizationID,
        network:        network,
        subscriptions:  make(map[string]*Subscription),
        listeners:      make(map[UpdateMethod][]func(string, *Subscription)),
        done:           make(chan struct{}),
    }
}

func (c *UpdateServiceClient) Connect() error {
    conn, _, err := websocket.DefaultDialer.Dial(c.url, nil)
    if err != nil {
        return err
    }
    c.conn = conn
    
    // Read Connected message
    _, msg, err := conn.ReadMessage()
    if err != nil {
        return err
    }
    
    if string(msg) != "Connected" {
        return fmt.Errorf("unexpected response: %s", msg)
    }
    
    fmt.Println("Connected to update service")
    
    // Start keep-alive
    go c.keepAlive()
    
    // Start message handler
    go c.handleMessages()
    
    return nil
}

func (c *UpdateServiceClient) Subscribe(method UpdateMethod, entityID string) error {
    sub := &Subscription{
        Network:        c.network,
        OrganizationID: c.organizationID,
        Method:         int(method),
    }
    
    if entityID != "" {
        sub.ID = entityID
    }
    
    msg := Message{
        Action:       ActionSubscribe,
        Subscription: sub,
    }
    
    key := c.getKey(method, entityID)
    c.mu.Lock()
    c.subscriptions[key] = sub
    c.mu.Unlock()
    
    return c.conn.WriteJSON(msg)
}

func (c *UpdateServiceClient) Unsubscribe(method UpdateMethod, entityID string) error {
    sub := &Subscription{
        Network:        c.network,
        OrganizationID: c.organizationID,
        Method:         int(method),
    }
    
    if entityID != "" {
        sub.ID = entityID
    }
    
    msg := Message{
        Action:       ActionUnsubscribe,
        Subscription: sub,
    }
    
    key := c.getKey(method, entityID)
    c.mu.Lock()
    delete(c.subscriptions, key)
    c.mu.Unlock()
    
    return c.conn.WriteJSON(msg)
}

func (c *UpdateServiceClient) On(method UpdateMethod, callback func(string, *Subscription)) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.listeners[method] = append(c.listeners[method], callback)
}

func (c *UpdateServiceClient) Disconnect() error {
    closeMsg := Message{Action: ActionClose}
    if err := c.conn.WriteJSON(closeMsg); err != nil {
        return err
    }
    
    close(c.done)
    return c.conn.Close()
}

func (c *UpdateServiceClient) keepAlive() {
    ticker := time.NewTicker(5 * time.Second)
    defer ticker.Stop()
    
    for {
        select {
        case <-ticker.C:
            if err := c.conn.WriteMessage(websocket.TextMessage, []byte("ping")); err != nil {
                fmt.Printf("Keep-alive error: %v\n", err)
                return
            }
        case <-c.done:
            return
        }
    }
}

func (c *UpdateServiceClient) handleMessages() {
    for {
        _, message, err := c.conn.ReadMessage()
        if err != nil {
            fmt.Printf("Read error: %v\n", err)
            return
        }
        
        msgStr := string(message)
        
        if len(msgStr) > 4 && msgStr[:4] == "pong" {
            newInstanceID := ""
            if len(msgStr) > 5 {
                newInstanceID = msgStr[5:]
            }
            
            if c.instanceID != "" && c.instanceID != newInstanceID {
                fmt.Println("Instance ID changed, resubscribing...")
                c.resubscribeAll()
            }
            c.instanceID = newInstanceID
            continue
        }
        
        var msg Message
        if err := json.Unmarshal(message, &msg); err != nil {
            fmt.Printf("JSON parse error: %v\n", err)
            continue
        }
        
        if msg.Action == ActionResponse && msg.Subscription != nil {
            method := UpdateMethod(msg.Subscription.Method)
            entityID := msg.Subscription.ID
            
            c.mu.RLock()
            callbacks := c.listeners[method]
            c.mu.RUnlock()
            
            for _, callback := range callbacks {
                go callback(entityID, msg.Subscription)
            }
        }
    }
}

func (c *UpdateServiceClient) resubscribeAll() {
    c.mu.RLock()
    subscriptions := make([]*Subscription, 0, len(c.subscriptions))
    for _, sub := range c.subscriptions {
        subscriptions = append(subscriptions, sub)
    }
    c.mu.RUnlock()
    
    for _, sub := range subscriptions {
        msg := Message{
            Action:       ActionSubscribe,
            Subscription: sub,
        }
        if err := c.conn.WriteJSON(msg); err != nil {
            fmt.Printf("Resubscribe error: %v\n", err)
        }
    }
}

func (c *UpdateServiceClient) getKey(method UpdateMethod, entityID string) string {
    if entityID != "" {
        return fmt.Sprintf("%d:%s", method, entityID)
    }
    return fmt.Sprintf("%d", method)
}

// Usage Example
func main() {
    client := NewUpdateServiceClient(
        "wss://api.sologenic.org/api/v1/update/ws",
        "024e6e3e-59e6-4037-be4d-bfbb3894dbeb",
        1, // mainnet
    )
    
    if err := client.Connect(); err != nil {
        panic(err)
    }
    
    // Register callbacks
    client.On(MethodBalanceUpdate, func(entityID string, sub *Subscription) {
        fmt.Printf("Balance updated for: %s\n", entityID)
        // Fetch fresh balance
        // balance := fetchBalance(entityID)
        // fmt.Printf("New balance: %v\n", balance)
    })
    
    client.On(MethodNotification, func(notificationID string, sub *Subscription) {
        fmt.Printf("New notification: %s\n", notificationID)
        // Fetch notification details
    })
    
    // Subscribe to updates
    client.Subscribe(MethodBalanceUpdate, "r123456789")
    client.Subscribe(MethodNotification, "")
    
    // Keep running
    select {}
}
Environment Variables
Variable	Description	Required
ORGANIZATION_STORE	Organization service endpoint	Yes
COMMENT_STORE	Comment service endpoint	Yes
AED_STORE	AED data endpoint	Yes
ASSET_STORE	Asset service endpoint	Yes
USER_STORE	User service endpoint	Yes
HTTP_CONFIG	HTTP server configuration	Yes
PROJECT_ID	GCP project ID (listener)	Yes
HTTP_PORT	Health probe port	Yes
CREDENTIALS_LOCATION	GCP credentials file path	Yes
APP_NAME	Application identifier	Yes
GRPC_APPEND	gRPC service name suffix	No
SUB_CONFIG	PubSub subscription config (JSON)	Yes
SUB_CONFIG Example
json
{
  "subscription_id": "update-service-sub",
  "topic": "com-trigger",
  "endpoint": "https://update-service:8080/push"
}
Docker Compose Example
yaml
version: '3.8'

services:
  update-service:
    image: sologenic/update-service:latest
    environment:
      - ORGANIZATION_STORE=organization-store:50062
      - COMMENT_STORE=comment-store:50063
      - AED_STORE=aed-store:50064
      - ASSET_STORE=asset-store:50056
      - USER_STORE=user-store:50049
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
      - PROJECT_ID=my-gcp-project
      - HTTP_PORT=8080
      - CREDENTIALS_LOCATION=/app/credentials.json
      - APP_NAME=update-service
      - LOG_LEVEL=info
    ports:
      - "8080:8080"
    volumes:
      - ./credentials.json:/app/credentials.json
    networks:
      - internal

  organization-store:
    image: sologenic/organization-store:latest
    networks:
      - internal

networks:
  internal:
    driver: bridge
Error Handling
Scenario	Behavior	Recovery
Connection lost	WebSocket closes	Client should reconnect
Instance ID change	Server restarted	Client resubscribes automatically
Ping timeout	Connection dropped	Client reconnects
Invalid subscription	Error message	Check method enum value
Best Practices
Connection Management
Send ping every 5 seconds

Handle instance ID changes by resubscribing

Use CLOSE action instead of abrupt disconnection

Implement reconnection logic with exponential backoff

Subscription Management
Subscribe only to needed topics

Unsubscribe when no longer needed

Store subscription state for resubscription

Use entity IDs for targeted updates

Performance
Limit number of simultaneous subscriptions

Cache frequently accessed data

Use event-driven pattern for rare updates

Use time-period pattern for frequent updates

Security
Always include OrganizationID header

Validate network parameter

Don't expose sensitive IDs in logs

Use WSS in production

Troubleshooting
Issue	Possible Cause	Solution
Connection drops	No ping sent	Send ping every 5 seconds
Missing updates	Wrong subscription	Verify method enum value
Duplicate updates	Multiple subscriptions	Track active subscriptions
Slow reconnection	Backoff too long	Implement exponential backoff
Instance ID changes	Service restart	Auto-resubscribe on change
Limitations
Current Limitations
Singleton deployment - Only one instance can run due to PubSub consumer implementation

No message replay - New consumers read from current position, not from start

Slow startup - Reading from topic start can cause minute-long delays

Future Improvements
Multiple consumer support with dynamic group IDs

Configurable start position (beginning/end)

Isolated listener services to reduce dependencies

New PubSub topic with complete data messages

Related Services
Service	Description
Organization Store	Tenant isolation
Comment Store	Comment replies
AED Store	Chart data
Asset Store	Asset metadata
User Store	User information
PubSub	Message bus
License
This documentation is part of the TX Marketplace platform.
