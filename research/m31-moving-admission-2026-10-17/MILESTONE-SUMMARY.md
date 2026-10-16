# Moving-state checkpoint: promising evidence, qualification failed

Two 64-drone local3D Boids groups completed ten seconds. We preserved actual tilt, motor thrust, velocity and rotation states at 0, 5, 10 seconds. All six snapshots passed their individual aerodynamic numerical checks at the four frozen 1e-8 normalized tolerances. Both runs changed relative 3D geometry and positive interaction edges, so this was not simply a translating static scene.

The overall checkpoint FAILED. All four fixed controls passed and all 20 deliberate corruptions were rejected, but one corruption hit a work-counter check before reaching its required semantic rule. Thus 19/20 met the registered control criterion. The official checker reports passed=false and advancement=false. We retain that result and do not repair or rerun this allocation.

This tells us that the unchanged model can produce individually checked results on these six moving states, subject to incomplete checker qualification. It does not establish a generally usable moving-state oracle. The next decision must address the validation gap in a fresh, publicly frozen allocation before browser transfer.

The Three.js replay shows two saved flights, 51 pose frames each. Only six full states were force-tested. Airflow was off during generation; posthoc aerodynamic queries did not change the flight. Playback is not a speed benchmark. Physical validity, closed-loop aerodynamic flight, 5,000-drone browser performance and novelty remain unestablished.

Source was public and independently verified before execution at 2a957d2b0bb26e731c8cd184bc13f51f673e9a0d. Kernel and checker each ran once and closed under their resource limits. Raw records, independent references, failed control details, reviews and exact provenance are preserved beside this summary.
