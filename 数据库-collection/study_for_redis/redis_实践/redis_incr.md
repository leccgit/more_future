
# INCR key

```markdown
Adapted from http://redis.io/commands/incr#pattern-rate-limiter-2
该命令从1.0.0起可用 时间复杂度为O（1） 将存储在key上的数字加一。如果key不存在，在执行操作之前将其值设置为0。如果key包含错误类型的值或包含不能表示为整数的字符串，则返回错误。此操作仅限于64位有符号整数。

redis> incr my_age
(integer) 1 redis> get my_age
"1"
redis> SET my_key "10"
"OK"
redis> INCR my_key
(integer) 11 redis> GET my_key
"11"
注意：这是一个字符串操作，因为Redis没有专用整数类型。存储在key上的字符串被解释为执行操作的基于-10 64位有符号整数。 Redis将整数存储在其整数表示形式中，因此对于实际持有整数的字符串值，存储整数的字符串表示没有开销。
```

## 1. 计数器

```markdown
计数器是使用Redis原子增量操作所能做的最明显的事情。每次操作发生时，只需向Redis发送INCR命令。 例如，在Web应用程序中，我们可能想知道该用户一年中每天浏览了多少页面。 为此，Web应用程序可以简单地在用户执行页面视图时incr
key，使用用户的唯一ID和表示当前日期的字符串作为key的名称。 这个模式可以通过多种方式扩展:
可以在每个页面视图中一起使用INCR和EXPIRE，以计数器仅计数最新的N页面视图，间隔小于指定秒数。 客户端可以使用GET,SET原子获取当前计数器值并将其重置为零。
使用DECR或INCRBY等其他原子增量/减量命令，可以处理根据用户执行的操作而可能越来越大或变小的值。例如，想象一下在线游戏中不同用户的分数。
```

## 2. redis实现评率限制器

```markdown
速率限制器模式是一种特殊的计数器，用于限制可以执行操作的速度。这种模式的经典实现涉及限制可以根据公共API执行的请求数量。
我们使用INCR提供了这种模式的两个实现，我们假设要解决的问题是将API调用的数量限制在每个IP地址最多每秒十个请求。 
```

### 2.1 实现1

```text
FUNCTION LIMIT_API_CALL(ip)
ts = CURRENT_UNIX_TIME()
keyname = ip+":"+ts
MULTI
    INCR(keyname)
    EXPIRE(keyname,10)
EXEC current = RESPONSE_OF_INCR_WITHIN_MULTI
IF current > 10 THEN
    ERROR "too many requests per second"
ELSE
    PERFORM_API_CALL()
END
基本上，我们为每个IP、每个不同秒都有一个计数器。但此计数器总是增量设置10秒的过期，以便在当前秒是不同的秒时，Redis会自动删除它们。 注意使用MULTI和EXEC的情况，以确保我们在每次API调用时都会增加和设置过期。
```

### 2.2 实现2

```markdown
替代实现使用单个计数器，但在没有竞争条件的情况下正确使用它有点复杂。我们将检查不同的变体。 FUNCTION LIMIT_API_CALL(ip):
current = GET(ip)
IF current != NULL AND current > 10 THEN ERROR "too many requests per second"
ELSE value = INCR(ip)
IF value == 1 THEN EXPIRE(ip,1)
END PERFORM_API_CALL()
END 计数器的创建方式只能存活一秒钟，从当前第二个执行的第一个请求开始。如果在同一秒有超过10个请求，计数器将达到大于10的值，否则它将过期，并从0重新开始。
在上述代码中有一个种族条件。如果客户端出于某种原因执行INCR命令，但没有执行EXPIRE，密钥将泄露，直到我们再次看到相同的IP地址。
```

```text
这可以很容易地将带有可选EXPIRE的INCR转换为使用EVAL命令发送的Lua脚本（仅自Redis版本2.6以来可用）。 
local current
current = redis.call("incr",KEYS[1])
if current == 1 then
    redis.call("expire",KEYS[1],1)
end
```

```text
有一种不同的方式可以在不使用脚本的情况下解决这个问题，而是使用Redis列表而不是计数器。实现更复杂，使用更高级的功能，但其优点是记住当前执行API调用的客户端的IP地址，这些地址可能有用或不有用，具体取决于应用程序。 FUNCTION
FUNCTION LIMIT_API_CALL(ip)
current = LLEN(ip)
IF current > 10 THEN
    ERROR "too many requests per second"
ELSE
    IF EXISTS(ip) == FALSE
        MULTI
            RPUSH(ip,ip)
            EXPIRE(ip,1)
        EXEC
    ELSE
        RPUSHX(ip,ip)
    END
    PERFORM_API_CALL()
END
RPUSHX命令只在键已经存在的情况下才推送元素。
注意，我们这里有一个竞争，但这不是一个问题:
    EXISTS可能返回false，但在我们在MULTI / EXEC块中创建键之前，它可能由另一个客户端创建。然而，这种竞争只会在极少数情况下错过一个API调用，所以速率限制仍然会正确工作。
```