export interface PropertySet {
  color: string;
  cards: number;
  isComplete: boolean;
  potentialRent: number;
}

export interface RentCalculation {
  totalPotentialRent: number;
  propertySets: PropertySet[];
  incompleteSets: PropertySet[];
  completeSets: PropertySet[];
}

// Rent values for each property color based on number of cards
export const RENT_VALUES = {
  'brown': [1, 2],           // 1-2 cards
  'dark-blue': [3, 8],       // 1-2 cards  
  'green': [2, 4, 7],        // 1-3 cards
  'light-blue': [1, 2, 3],   // 1-3 cards
  'orange': [1, 3, 5],       // 1-3 cards
  'magenta': [1, 2, 4],      // 1-3 cards (purple)
  'black': [1, 2, 3, 4],    // 1-4 cards (railroad)
  'red': [2, 3, 6],          // 1-3 cards
  'submarine': [1, 2],       // 1-2 cards (utility)
  'yellow': [2, 4, 6],       // 1-3 cards
};

// Wild card color mappings
export const WILD_CARD_COLORS = {
  'purple-orange': ['magenta', 'orange'],
  'light-blue-brown': ['light-blue', 'brown'],
  'light-blue-railroad': ['light-blue', 'black'],
  'dark-blue-green': ['dark-blue', 'green'],
  'railroad-green': ['black', 'green'],
  'red-yellow': ['red', 'yellow'],
  'utility-railroad': ['submarine', 'black'],
  'multi-color': ['brown', 'dark-blue', 'green', 'light-blue', 'orange', 'magenta', 'black', 'red', 'submarine', 'yellow']
};

// Calculate rent for a specific property color and number of cards
export function calculateRentForColor(color: string, cardCount: number): number {
  const rentValues = RENT_VALUES[color as keyof typeof RENT_VALUES];
  if (!rentValues) return 0;
  
  // Return the rent for the given number of cards (1-based index)
  return rentValues[Math.min(cardCount - 1, rentValues.length - 1)] || 0;
}

// Calculate potential rent for a property set
export function calculatePropertySetRent(color: string, cardCount: number): PropertySet {
  const potentialRent = calculateRentForColor(color, cardCount);
  const maxCards = RENT_VALUES[color as keyof typeof RENT_VALUES]?.length || 0;
  const isComplete = cardCount >= maxCards;
  
  return {
    color,
    cards: cardCount,
    isComplete,
    potentialRent
  };
}

// Calculate total rent potential from all properties
export function calculateTotalRentPotential(properties: { [color: string]: any[] }): RentCalculation {
  const propertySets: PropertySet[] = [];
  let totalPotentialRent = 0;
  
  // Process regular properties
  Object.entries(properties).forEach(([color, cards]) => {
    if (cards && cards.length > 0) {
      const propertySet = calculatePropertySetRent(color, cards.length);
      propertySets.push(propertySet);
      totalPotentialRent += propertySet.potentialRent;
    }
  });
  
  // Separate complete and incomplete sets
  const completeSets = propertySets.filter(set => set.isComplete);
  const incompleteSets = propertySets.filter(set => !set.isComplete);
  
  return {
    totalPotentialRent,
    propertySets,
    completeSets,
    incompleteSets
  };
}

// Calculate rent potential including wild cards
export function calculateRentWithWildCards(
  properties: { [color: string]: any[] },
  wildCards: any[]
): RentCalculation {
  // Start with regular properties
  // const baseCalculation = calculateTotalRentPotential(properties);
  
  // Create a copy to work with
  const enhancedProperties = { ...properties };
  
  // Process wild cards to maximize rent potential
  wildCards.forEach(wildCard => {
    if (wildCard.color === 'multi') {
      // Multi-color wild card - find the best color to assign it to
      let bestColor = '';
      let bestRentIncrease = 0;
      
      Object.entries(RENT_VALUES).forEach(([color]) => {
        const currentCards = enhancedProperties[color]?.length || 0;
        const currentRent = calculateRentForColor(color, currentCards);
        const newRent = calculateRentForColor(color, currentCards + 1);
        const rentIncrease = newRent - currentRent;
        
        if (rentIncrease > bestRentIncrease) {
          bestRentIncrease = rentIncrease;
          bestColor = color;
        }
      });
      
      // Assign wild card to the color that gives the best rent increase
      if (bestColor) {
        if (!enhancedProperties[bestColor]) {
          enhancedProperties[bestColor] = [];
        }
        enhancedProperties[bestColor].push(wildCard);
      }
    } else if (wildCard.description && wildCard.description.includes('Wild property card')) {
      // Two-color wild card - find the best of the two colors
      const wildCardColors = getWildCardColors(wildCard);
      if (wildCardColors.length === 2) {
        let bestColor = wildCardColors[0];
        let bestRentIncrease = 0;
        
        wildCardColors.forEach(color => {
          const currentCards = enhancedProperties[color]?.length || 0;
          const currentRent = calculateRentForColor(color, currentCards);
          const newRent = calculateRentForColor(color, currentCards + 1);
          const rentIncrease = newRent - currentRent;
          
          if (rentIncrease > bestRentIncrease) {
            bestRentIncrease = rentIncrease;
            bestColor = color;
          }
        });
        
        // Assign wild card to the color that gives the best rent increase
        if (!enhancedProperties[bestColor]) {
          enhancedProperties[bestColor] = [];
        }
        enhancedProperties[bestColor].push(wildCard);
      }
    }
  });
  
  // Recalculate with enhanced properties
  return calculateTotalRentPotential(enhancedProperties);
}

// Get the colors that a wild card can represent
export function getWildCardColors(wildCard: any): string[] {
  if (wildCard.color === 'multi') {
    return Object.keys(RENT_VALUES);
  }
  
  // Check if it's a two-color wild card
  if (wildCard.description && wildCard.description.includes('Wild property card')) {
    // Extract colors from the description or name
    const name = wildCard.name.toLowerCase();
    
    if (name.includes('purple') && name.includes('orange')) {
      return ['magenta', 'orange'];
    } else if (name.includes('light blue') && name.includes('brown')) {
      return ['light-blue', 'brown'];
    } else if (name.includes('light blue') && name.includes('railroad')) {
      return ['light-blue', 'black'];
    } else if (name.includes('dark blue') && name.includes('green')) {
      return ['dark-blue', 'green'];
    } else if (name.includes('railroad') && name.includes('green')) {
      return ['black', 'green'];
    } else if (name.includes('red') && name.includes('yellow')) {
      return ['red', 'yellow'];
    } else if (name.includes('utility') && name.includes('railroad')) {
      return ['submarine', 'black'];
    }
  }
  
  return [];
}

// Format rent calculation for display
export function formatRentCalculation(calculation: RentCalculation): string {
  const { totalPotentialRent, completeSets, incompleteSets } = calculation;
  
  let result = `Total Potential Rent: $${totalPotentialRent}M\n\n`;
  
  if (completeSets.length > 0) {
    result += `Complete Sets:\n`;
    completeSets.forEach(set => {
      result += `  ${set.color}: ${set.cards} cards = $${set.potentialRent}M rent\n`;
    });
    result += '\n';
  }
  
  if (incompleteSets.length > 0) {
    result += `Incomplete Sets:\n`;
    incompleteSets.forEach(set => {
      const maxCards = RENT_VALUES[set.color as keyof typeof RENT_VALUES]?.length || 0;
      const remainingCards = maxCards - set.cards;
      result += `  ${set.color}: ${set.cards}/${maxCards} cards = $${set.potentialRent}M rent (need ${remainingCards} more for max rent)\n`;
    });
  }
  
  return result;
}
