import pandas as pd
import os, sys

# Load the CSV file
script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
file_path = script_directory + '/destinyArmor.csv'
df = pd.read_csv(file_path)

# Define the perk options for each entry
perk_options = {
    'Relativism': {
        'title': 'Hunter - Relativism',
        'left': [
            'Spirit of the Assassin', 'Spirit of Inmost Light', 'Spirit of the Ophidian',
            'Spirit of the Dragon', 'Spirit of Galanor', 'Spirit of the Foetracer',
            'Spirit of Caliban', 'Spirit of Renewal'
        ],
        'right': [
            'Spirit of the Star-Eater', 'Spirit of Synthoceps', 'Spirit of Verity',
            'Spirit of the Cyrtarachne', 'Spirit of the Gyrfalcon', 'Spirit of the Liar',
            'Spirit of the Wormhusk', 'Spirit of the Coyote'
        ]
    },
    'Stoicism': {
        'title': 'Titan - Stoicism',
        'left': [
            'Spirit of the Assassin', 'Spirit of Inmost Light', 'Spirit of the Ophidian',
            'Spirit of Severance', 'Spirit of Hoarfrost', 'Spirit of the Eternal Warrior',
            'Spirit of the Abeyant', 'Spirit of the Bear'
        ],
        'right': [
            'Spirit of the Star-Eater', 'Spirit of Synthoceps', 'Spirit of Verity',
            'Spirit of Contact', 'Spirit of Scars', 'Spirit of the Horn',
            'Spirit of Alpha Lupi', 'Spirit of the Armamentarium'
        ]
    },
    'Solipsism': {
        'title': 'Warlock - Solipsism',
        'left': [
            'Spirit of the Assassin', 'Spirit of Inmost Light', 'Spirit of the Ophidian',
            'Spirit of the Stag', 'Spirit of the Filaments', 'Spirit of the Necrotic',
            'Spirit of Osmiomancy', 'Spirit of Apotheosis'
        ],
        'right': [
            'Spirit of the Star-Eater', 'Spirit of Synthoceps', 'Spirit of Verity',
            'Spirit of Vesper', 'Spirit of Harmony', 'Spirit of Starfire',
            'Spirit of the Swarm', 'Spirit of the Claw'
        ]
    }
}


# Function to generate the CSV for a given entry with improved soft matching ensuring all entries are represented
def generate_csv_for_entry_complete(entry_name):
    entry_df = df[df['Name'] == entry_name]
    
    # Extract relevant perks columns and filter for the perk options
    perks_columns = [col for col in entry_df.columns if col.startswith('Perks')]
    entry_df = entry_df[perks_columns]
    
    left_perks = perk_options[entry_name]['left']
    right_perks = perk_options[entry_name]['right']
    
    # Create a dictionary to hold the count of each combination
    combinations = {(left, right): 0 for left in left_perks for right in right_perks}
    
    # Count the combinations
    for _, row in entry_df.iterrows():
        perks = row.dropna().tolist()
        left_perk = next((perk for perk in perks if any(left in perk for left in left_perks)), None)
        right_perk = next((perk for perk in perks if any(right in perk for right in right_perks)), None)
        
        if left_perk and right_perk:
            left_match = next(left for left in left_perks if left in left_perk)
            right_match = next(right for right in right_perks if right in right_perk)
            combinations[(left_match, right_match)] += 1
    
    # Create a DataFrame for the combinations
    combination_df = pd.DataFrame.from_dict(combinations, orient='index', columns=['Count']).reset_index()
    combination_df[['Left Perk', 'Right Perk']] = pd.DataFrame(combination_df['index'].tolist(), index=combination_df.index)
    combination_df.drop(columns=['index'], inplace=True)
    
    # Pivot the DataFrame to get the desired format
    pivot_df = combination_df.pivot(index='Left Perk', columns='Right Perk', values='Count').fillna(0)
    
    # Ensure the order of the axes matches the perk option entry order
    pivot_df = pivot_df.reindex(index=left_perks, columns=right_perks)
    
    # Add the title in the top-left cell
    pivot_df.index.name = perk_options[entry_name]['title']
    pivot_df.columns.name = ''
    
    # Save to CSV
    pivot_df.to_csv(f'Downloads/{entry_name}_perk_combinations_complete.csv')

# Generate CSVs for all three entries ensuring all are represented
for entry in perk_options.keys():
    generate_csv_for_entry_complete(entry)

