## Data Access
The data in our project is about the world configurations, including the locations and people and their description in the town. The data is stored `world_config.json`. You can find it here: [simulation/environment/world_config.json](https://github.com/Sssssimonk/DSC180_B16_Generative_Agents/blob/main/simulation/environment/world_config.json).

## Set Up
### Launch the Server
After login to DSMLP, run the following commands:
```bash
launch-scipy-ml.sh -W DSC180A_FA23_A00 -c 8 -m 64 -g 2 -p low
```

### Software Dependencies
The librabries and packages is in [requirements.txt](https://github.com/Sssssimonk/DSC180_B16_Generative_Agents/blob/main/requirements.txt). To install these dependencies, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

This command should be executed in the environment where you intend to run the project. It will automatically install all the libraries and packages specified in the requirements.txt file.

## Reproducing Results
To run the simulation, you simply need to run the `main.py `. This file will call the functions we defined in other files, so it is the primary entry point for our project and executes the necessary code to generate the results.
### Running `main.py`
Follow these steps to run `main.py`:
1. **Open Terminal or Command Line:**
   - Navigate to the directory simulation, where `main.py` is located.
2. **Execute the Script:**
   - Run the following command:
   ```bash
   python main.py
   ```
   - Note: After running the command, you will be ask to input a number to limit the times of generating results. Please enter a positive integer less than 10.
