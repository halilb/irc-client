# irc-client

This is the client code running a simple messaging protocol.

### Requirements

This client works well with Python 2.7.10. Other versions are not tested.
You also need to have [PyQt](https://wiki.python.org/moin/PyQt) on your computer as it is used to build client's interface.

### Running

You must provide server hostname and port address.

```bash
python main.py <hostname> <portaddress>
```

### Tests

You have to install [nose](https://nose.readthedocs.org/en/latest/) to run unit tests.

```bash
pip install nose
python main.py <hostname> <portaddress>
```

### Code Structure

There are 3 main components running on different threads.

#### 1.Interface
Interface is built on top of the PyQt library. It draws a desktop interface for user input, incoming messages and user list.

When user clicks send button, user's message is put in threadQueue without any manipulation. That message is parsed in **Writer** object.
 
Interface also consumes **screenQueue** form transforming network messages to end user messages according to the chat protocol.

#### 2. Writer
This component communicates with Interface via threadQueue. It parses user messages into protocol messages and send it over TCP. 

#### 3. Reader
This component listens server messages and parses them into **IncomingMessage** object. It decides the type of message and related username. After parsing process, it puts IncomingMessage object to screenQueu.

### Server Problems

I experienced 2 problems with the server:
- Server sometimes closes the TCP connection when i try to register a new user name(/nick halil)
- Server does not end messages with new line character(\n). This prevents me from parsing multiple messages within one TCP stream.(TICSAY halil:hello)
