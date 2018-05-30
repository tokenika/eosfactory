## 1. Test3 fails FIXED
```
Name is longer than 13 characters (_e4b2ffc804529ce9c6fae258197648cc2)
```

## 2. Tasks compile & build fail FIXED
```
/bin/bash: generate: command not found
/bin/bash: build: command not found
```

## 3. Skeleton name verifcation should be before contract folder is created FIXED
Otherwise the user is confused during a second attempt: 
```
ERROR!
{"sender":" | build_contract.cpp[177](bootstrapContract) | ", "message":{Contract
/mnt/x/Workspaces/EOS/contracts/hello.teos33
 workspace already exists. Cannot owerwrite it.}}
 ```

## 4. Confusing output during build FIXED
```
Scanning dependencies of target abi
ERROR!
An ABI exists in the source directory. Cannot overwrite it:
```

## 5. Confusing output when a unit-test failure is desired  FIXED
```
.ERROR!
status code is 500
 eosd response is Content-Length: 350
Content-type: application/json
Server: WebSocket++/0.7.0

{"code":500,"message":"Internal Service Error","error":{"code":3090004,"name":"missing_auth_exception","what":"missing required authority","details":[{"message":"missing authority of carol","file":"apply_context.cpp","line_number":119,"method":"require_authorization"},{"message":"","file":"apply_context.cpp","line_number":55,"method":"exec_one"}]}}
```