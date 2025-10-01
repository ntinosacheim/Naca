```{mermaid}
classDiagram
    direction TB
    
    class Hansen_Algorithm {
        +float tolerance
        +int max_iter
        %% +list r_is
        %% +list chords
        %% +list pitch
        %% +list tc_ratios
        %% +int no_sections
        %% +float R
        %% +int B
        %% +float air_density
        %% -calculation_of_flow_angle_rad(a, a_p, r, v0, w_rps) float -->
        %% -calculation_of_local_angle_of_attack_rad(flow_angle_rad, pitch_angle_deg, twist_deg) float -->
        %% -calculation_of_Cl_and_Cd(angle_of_attack_deg, tc_ratio) tuple
        %% -calculation_of_Cn_and_Ct(Cl, Cd, flow_angle_rad) tuple
        %% -calculation_of_updated_induction_factors(Cn, Ct, r, chord, flow_angle_rad) tuple
        %% -calculation_of_local_loads(r, a, a_p, v0, w_rps, chord, %%flow_angle_rad, Cl, Cd) tuple
        +segment_calculation(V0, ω , r, c,  pitch, twist, tc_ratio, f) 
        +DTU_blade_calculation(wind_speed_V0, rotation_speed) 
        %%-calculation_of_coefficient_of_power_cp_for_DTU(total_power, wind_speed_V0) float
        %%-calculation_of_coefficient_of_thrust_CT_for_DTU(total_thrust, wind_speed_V0) float
    }

    class DTU_calc {
        -set tc_values
        +__init__(csv_data_file_DTU)
        -load_data(csv_data_file_DTU) void
        %%-linear_interpolation(x, x1, x2, y1, y2) float
        %%-get_nearest_value(values, desired_value) tuple
        %%-get_interpolated_value(angle_of_attack, tc_ratio, coef) float
        +cl(angle_of_attack, tc_ratio) float
        +cd(angle_of_attack, tc_ratio) float
        +cm(angle_of_attack, tc_ratio) float
    }

    class Main_Execution {
    }
    
    class Excel_to_CSV {
        +convert_excel_to_csv(excel_file, output_csv)
    }

    Hansen_Algorithm "1" *-- "1" DTU_calc : uses
    Main_Execution ..> Hansen_Algorithm : instantiates
    Main_Execution ..> DTU_calc : instantiates indirectly
```