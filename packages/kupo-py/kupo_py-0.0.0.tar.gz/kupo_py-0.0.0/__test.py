from kupo import KupoClient
from kupo.utils import ERA_BOUNDARIES

from charli3_dendrite.dexs.core.base import AbstractPairState
from pycardano import Address

# Get all DEX classes
subclass_walk = [AbstractPairState]
D: list[AbstractPairState] = []

while len(subclass_walk) > 0:
    c = subclass_walk.pop()

    subclasses = c.__subclasses__()

    # If no subclasses, this is a a DEX class. Ignore MuesliCLP for now
    try:
        if isinstance(c.dex(), str) and c.__name__ not in ["MuesliSwapCLPState"]:
            c.pool_selector()
            D.append(c)
            subclass_walk.extend(subclasses)
        else:
            subclass_walk.extend(subclasses)
    except NotImplementedError:
        subclass_walk.extend(subclasses)

D = list(sorted(set(D), key=lambda d: d.__name__))

# Get currently tracked patterns
# client = KupoClient(base_url="http://localhost", port=1442)

# current_patterns = [p.root for p in client.get_patterns()]
current_patterns = []

# Generate a list of all pool scripts not currently tracked
pool_scripts = []
for d in D:
    if d.dex() == "Axo":
        continue
    addresses = d.pool_selector().addresses
    for address in addresses:
        script_hash = Address.decode(address).payment_part.payload.hex()
        pattern = f"{script_hash}/*"

        if pattern in current_patterns:
            print(f"Pattern for {d.dex()} is already being tracked: {pattern}")
            continue
        pool_scripts.append(f"{script_hash}/*")

pool_scripts = list(set(pool_scripts))

print(f"New patterns to track: {len(pool_scripts)}")

# # Start tracking untracked patterns
# for pattern in pool_scripts:
#     patterns = client.add_pattern(
#         pattern=pattern, rollback_to=ERA_BOUNDARIES["last_mary_block"]
#     )
#     print(patterns)
#     break

print(pool_scripts)
# print(current_patterns)
