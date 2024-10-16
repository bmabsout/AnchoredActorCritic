trap 'kill $(jobs -p)' EXIT

# Original
python -m envs.LunarLander.test_lander trained/lander-custom/a_n:0.01,e:50,l:0.001,s_s:10000,x:YQJBZMB5V5LRVHI/seeds/*/epochs/49 --initial-random 1500.0 --store_results results/lander/original/Source.pkl &
sleep 1
python -m envs.LunarLander.test_lander trained/lander-custom/a_n:0.01,e:50,l:0.001,s_s:10000,x:YQJBZMB5V5LRVHI/seeds/*/epochs/49 --initial-random 100.0 --store_results results/lander/original/Target.pkl &
sleep 1

# Naive
python -m envs.LunarLander.test_lander trained/lander-custom/a_n:0.001,e:14,l:1e-05,p*/seeds/1/epochs/13 --store_results results/lander/naive/Source.pkl -w &
sleep 1
python -m envs.LunarLander.test_lander trained/lander-custom/a_n:0.001,e:14,l:1e-05,p*/seeds/1/epochs/13 --store_results results/lander/naive/Target.pkl &
sleep 1

# Anchored
python -m envs.LunarLander.test_lander trained/lander-custom/a:True,a_n:0.001,e:14,l:1e-05,p*/seeds/1/epochs/13 --store_results results/lander/anchored/Source.pkl -w &
sleep 1
python -m envs.LunarLander.test_lander trained/lander-custom/a:True,a_n:0.001,e:14,l:1e-05,p*/seeds/1/epochs/13 --store_results results/lander/anchored/Target.pkl &


wait
