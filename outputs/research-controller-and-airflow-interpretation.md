# Interpreting the airflow failures

The corrected study holds the navigation rules and controller fixed while changing assumed loads. It therefore tests a **model–controller combination**. A failed mission is not a proof that the route is physically impossible, nor that one airflow formula is accurate.

The baseline inner flight controller receives desired velocity from the local flock rules. The interface converts desired vertical velocity into a moving altitude reference. At level attitude, its nominal vertical acceleration request simplifies to g +2.5(v_des,z −v_z), before limits. There is no dedicated integral or model-based downwash compensation in this interface. The shared route supplies outer position guidance, but desired velocity remains bounded.

A simple algebraic diagnostic illustrates the consequence. At zero actual vertical velocity, a desired climb of0.9m/s (the command-speed bound) produces nominal vertical thrust only1.2294 times weight. Under a hypothetical constant lift-retention factor below0.8134, that steady request cannot balance gravity. The nominal motor limit is a separate2.25× authority bound; the controller need not reach it while actual vertical velocity is zero. Once a drone descends, velocity feedback can request more thrust, so this is not a claim about every transient state.

[The diagnostic](milestone-28-control-authority.json) evaluates the actual frozen control function at the stated conditions and verifies the algebra. It does not assume constant lift loss in the mission simulations, fit measurements or explain each failure’s exact cause. Actual inflow varies with neighbors, attitude, position and time; route and obstacle feedback also change commands.

The practical implication is to retain these results as a sensitivity benchmark for an uncompensated baseline. A future compensation controller would require its own frozen matched comparison and realistic actuator/force validation. Quietly adding compensation to make the current cases pass would change the experiment. The present evidence does not establish physical impossibility or a validated safe operating envelope.
