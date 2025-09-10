import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { ArrowRight, Plus, Wallet, Home, Car, Users, Settings } from 'lucide-react';
import ConfigurationPanel from '../components/ConfigurationPanel';

interface Card {
  id: string;
  name: string;
  type: 'property' | 'money' | 'action' | 'building';
  color?: string;
  value?: number;
  description?: string;
  count?: number;
}

// Complete deck data with proper counts
const COMPLETE_DECK = {
  action: [
    { id: "deal_breaker_1", name: "Deal Breaker", type: "action", color: "red", description: "Steal a complete property set", count: 2 },
    { id: "just_say_no_1", name: "Just Say No", type: "action", color: "blue", description: "Cancel any action card", count: 3 },
    { id: "sly_deal_1", name: "Sly Deal", type: "action", color: "purple", description: "Steal a property from any player", count: 3 },
    { id: "force_deal_1", name: "Force Deal", type: "action", color: "orange", description: "Swap a property with any player", count: 4 },
    { id: "debt_collector_1", name: "Debt Collector", type: "action", color: "yellow", description: "Take $5M from any player", count: 3 },
    { id: "birthday_1", name: "It's My Birthday", type: "action", color: "pink", description: "All players give you $2M", count: 3 },
    { id: "pass_go_1", name: "Pass Go", type: "action", color: "green", description: "Draw 2 cards", count: 10 },
    { id: "house_1", name: "House", type: "building", color: "brown", description: "Add to a complete property set", count: 3 },
    { id: "hotel_1", name: "Hotel", type: "building", color: "brown", description: "Add to a complete property set", count: 3 },
    { id: "double_rent_1", name: "Double The Rent", type: "action", color: "gold", description: "Double the rent you collect", count: 2 }
  ],
  property: [
    { id: "brown_prop_1", name: "Brown Property", type: "property", color: "brown", value: 1, count: 2 },
    { id: "light_blue_prop_1", name: "Light Blue Property", type: "property", color: "light-blue", value: 1, count: 3 },
    { id: "pink_prop_1", name: "Pink Property", type: "property", color: "pink", value: 2, count: 3 },
    { id: "orange_prop_1", name: "Orange Property", type: "property", color: "orange", value: 2, count: 3 },
    { id: "red_prop_1", name: "Red Property", type: "property", color: "red", value: 3, count: 3 },
    { id: "yellow_prop_1", name: "Yellow Property", type: "property", color: "yellow", value: 3, count: 3 },
    { id: "green_prop_1", name: "Green Property", type: "property", color: "green", value: 4, count: 3 },
    { id: "dark_blue_prop_1", name: "Dark Blue Property", type: "property", color: "dark-blue", value: 4, count: 2 },
    { id: "railroad_prop_1", name: "Railroad Property", type: "property", color: "black", value: 2, count: 4 },
    { id: "utility_prop_1", name: "Utility Property", type: "property", color: "gray", value: 1, count: 2 }
  ],
  money: [
    { id: "money_1m_1", name: "$1M", type: "money", value: 1, color: "green", count: 6 },
    { id: "money_2m_1", name: "$2M", type: "money", value: 2, color: "blue", count: 5 },
    { id: "money_3m_1", name: "$3M", type: "money", value: 3, color: "red", count: 3 },
    { id: "money_4m_1", name: "$4M", type: "money", value: 4, color: "purple", count: 3 },
    { id: "money_5m_1", name: "$5M", type: "money", value: 5, color: "orange", count: 2 },
    { id: "money_10m_1", name: "$10M", type: "money", value: 10, color: "gold", count: 1 }
  ],
  wildcard: [
    { id: "wild_purple_orange_1", name: "Purple & Orange", type: "property", color: "multi", description: "Wild property card", count: 2 },
    { id: "wild_light_blue_brown_1", name: "Light Blue & Brown", type: "property", color: "multi", description: "Wild property card", count: 1 },
    { id: "wild_light_blue_railroad_1", name: "Light Blue & Railroad", type: "property", color: "multi", description: "Wild property card", count: 1 },
    { id: "wild_dark_blue_green_1", name: "Dark Blue & Green", type: "property", color: "multi", description: "Wild property card", count: 1 },
    { id: "wild_railroad_green_1", name: "Railroad & Green", type: "property", color: "multi", description: "Wild property card", count: 1 },
    { id: "wild_red_yellow_1", name: "Red & Yellow", type: "property", color: "multi", description: "Wild property card", count: 2 },
    { id: "wild_utility_railroad_1", name: "Utility & Railroad", type: "property", color: "multi", description: "Wild property card", count: 1 },
    { id: "wild_10color_1", name: "10-Color Wild", type: "property", color: "multi", description: "Wild property card", count: 2 }
  ],
  rent: [
    { id: "rent_purple_orange_1", name: "Purple & Orange Rent", type: "action", color: "multi", description: "Collect rent from purple or orange properties", count: 2 },
    { id: "rent_railroad_utility_1", name: "Railroad & Utility Rent", type: "action", color: "multi", description: "Collect rent from railroad or utility properties", count: 2 },
    { id: "rent_green_darkblue_1", name: "Green & Dark Blue Rent", type: "action", color: "multi", description: "Collect rent from green or dark blue properties", count: 2 },
    { id: "rent_brown_lightblue_1", name: "Brown & Light Blue Rent", type: "action", color: "multi", description: "Collect rent from brown or light blue properties", count: 2 },
    { id: "rent_red_yellow_1", name: "Red & Yellow Rent", type: "action", color: "multi", description: "Collect rent from red or yellow properties", count: 2 },
    { id: "rent_all_color_1", name: "All Color Wild Rent", type: "action", color: "multi", description: "Collect rent from any color properties", count: 3 }
  ]
};

const Dashboard: React.FC = () => {
  // Game state
  const [hand, setHand] = useState<Card[]>([]);
  const [properties, setProperties] = useState<{ [color: string]: Card[] }>({});
  const [money, setMoney] = useState<Card[]>([]);
  const [deck, setDeck] = useState(JSON.parse(JSON.stringify(COMPLETE_DECK)));

  // Card selection state
  const [selectedCards, setSelectedCards] = useState<string[]>([]);
  const [moveMode, setMoveMode] = useState<boolean>(false);
  const [moveTarget, setMoveTarget] = useState<string>('');
  const [wildPropertyColor, setWildPropertyColor] = useState<string>('');

  // Transfer state
  const [transferMode, setTransferMode] = useState<boolean>(false);
  const [transferTarget, setTransferTarget] = useState<number | ''>('');
  const [transferType, setTransferType] = useState<'properties' | 'money'>('properties');

  // Wild property selection state
  const [wildPropertySelection, setWildPropertySelection] = useState<{
    show: boolean;
    opponentId: number;
    wildType: string;
    availableColors: string[];
  }>({
    show: false,
    opponentId: 0,
    wildType: '',
    availableColors: []
  });

  // Opponent selection mode for deck
  const [opponentSelectionMode, setOpponentSelectionMode] = useState<{
    active: boolean;
    opponentId: number | null;
  }>({
    active: false,
    opponentId: null
  });

  // Opponent card transfer mode
  const [opponentTransferMode, setOpponentTransferMode] = useState<{
    active: boolean;
    sourceOpponentId: number | null;
    selectedCards: Array<{ cardId: string, cardType: 'property' | 'money', color?: string, index: number }>;
    targetOpponentId: number | null;
    targetType: 'properties' | 'money' | 'hand';
  }>({
    active: false,
    sourceOpponentId: null,
    selectedCards: [],
    targetOpponentId: null,
    targetType: 'properties'
  });

  // Opponents (example data)
  const [opponents, setOpponents] = useState<Array<{
    id: number;
    name: string;
    properties?: { [color: string]: Card[] };
    money?: Card[];
  }>>([
    { id: 1, name: "Player 1", properties: {}, money: [] },
    { id: 2, name: "Player 2", properties: {}, money: [] },
    { id: 3, name: "Player 3", properties: {}, money: [] },
  ]);

  // AI Analysis state
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<{
    recommendedMove: string;
    reasoning: string;
    strongestPlayer: string;
    winProbability: { [key: string]: number };
  } | null>(null);

  // Configuration state
  const [edgeRules, setEdgeRules] = useState({
    housePayment: 'bank' as 'bank' | 'incomplete_set' | 'floating',
    hotelMove: 'not_allowed' as 'not_allowed' | 'free_move' | 'costs_action',
    deckExhaustion: 'reshuffle' as 'reshuffle' | 'game_over',
    extraProperties: 'cap' as 'cap' | 'split',
    buildingForfeiture: 'discard' as 'discard' | 'to_bank' | 'keep_floating',
    propertyMerging: 'auto_merge' as 'auto_merge' | 'manual_merge' | 'no_merge',
    quadrupleRent: false,
    forcedDealToDealBreaker: true,
    justSayNoEmptyHand: true,
    justSayNoOnZero: true
  });

  const getCardColor = (color: string) => {
    const colorMap: { [key: string]: string } = {
      'brown': 'bg-amber-800',
      'light-blue': 'bg-cyan-400',
      'pink': 'bg-pink-400',
      'orange': 'bg-orange-500',
      'red': 'bg-red-500',
      'yellow': 'bg-yellow-500',
      'green': 'bg-green-500',
      'dark-blue': 'bg-blue-800',
      'railroad': 'bg-gray-800',
      'utility': 'bg-gray-500',
      'purple': 'bg-purple-600',
      'black': 'bg-gray-800',
      'gray': 'bg-gray-500',
      'blue': 'bg-blue-600',
      'gold': 'bg-yellow-400',
      'multi': 'bg-gradient-to-r from-purple-400 to-pink-400'
    };
    return colorMap[color] || 'bg-gray-400';
  };

  const getWildPropertyColors = (card: Card | string): string[] => {
    // Handle both Card objects and string wild types
    const wildType = typeof card === 'string' ? card : card.name;

    if (wildType.includes('Purple & Orange')) {
      return ['purple', 'orange'];
    } else if (wildType.includes('Light Blue & Brown')) {
      return ['light-blue', 'brown'];
    } else if (wildType.includes('Light Blue & Railroad')) {
      return ['light-blue', 'railroad'];
    } else if (wildType.includes('Dark Blue & Green')) {
      return ['dark-blue', 'green'];
    } else if (wildType.includes('Railroad & Green')) {
      return ['railroad', 'green'];
    } else if (wildType.includes('Red & Yellow')) {
      return ['red', 'yellow'];
    } else if (wildType.includes('Utility & Railroad')) {
      return ['utility', 'railroad'];
    } else if (wildType.includes('10-Color Wild')) {
      return ['brown', 'light-blue', 'pink', 'orange', 'red', 'yellow', 'green', 'dark-blue', 'railroad', 'utility'];
    }
    return [];
  };

  const hasWildProperties = () => {
    return selectedCards.some(cardId => {
      const card = hand.find(c => c.id === cardId);
      return card && card.type === 'property' && card.color === 'multi';
    });
  };

  const drawCard = (card: Card) => {
    // Remove one card from deck
    const newDeck = { ...deck };
    Object.values(newDeck).forEach((category: any) => {
      category.forEach((deckCard: any) => {
        if (deckCard.id === card.id && deckCard.count > 0) {
          deckCard.count--;
        }
      });
    });
    setDeck(newDeck);

    // Add to hand
    const cardToAdd = { ...card, id: `${card.id}_${Date.now()}` };
    setHand(prev => [...prev, cardToAdd]);
  };

  const toggleCardSelection = (cardId: string) => {
    setSelectedCards(prev =>
      prev.includes(cardId)
        ? prev.filter(id => id !== cardId)
        : [...prev, cardId]
    );
  };

  const startMove = () => {
    if (selectedCards.length > 0) {
      setMoveMode(true);
      setWildPropertyColor('');
    }
  };

  const startTransfer = () => {
    if (selectedCards.length > 0) {
      setTransferMode(true);
      setTransferTarget('');
      setTransferType('properties');
      setWildPropertyColor('');
    }
  };

  const cancelMove = () => {
    setMoveMode(false);
    setSelectedCards([]);
    setMoveTarget('');
    setWildPropertyColor('');
  };

  const cancelTransfer = () => {
    setTransferMode(false);
    setSelectedCards([]);
    setTransferTarget('');
    setTransferType('properties');
    setWildPropertyColor('');
  };

  const executeMove = () => {
    if (selectedCards.length > 0 && moveTarget) {
      const cardsToMove = hand.filter(card => selectedCards.includes(card.id));

      if (moveTarget === 'properties') {
        // Move to properties
        cardsToMove.forEach(card => {
          if (card.type === 'property') {
            let targetColor = card.color || 'other';

            // Handle wild properties - use selected color
            if (targetColor === 'multi' && card.description && card.description.includes('Wild property card')) {
              if (wildPropertyColor) {
                targetColor = wildPropertyColor;
              } else {
                // Fallback to first available color if none selected
                const availableColors = getWildPropertyColors(card);
                targetColor = availableColors[0] || 'other';
              }
            }

            setProperties(prev => ({
              ...prev,
              [targetColor]: [...(prev[targetColor] || []), card]
            }));
          }
        });
      } else if (moveTarget === 'money') {
        // Move to money pile
        cardsToMove.forEach(card => {
          if (card.type === 'money') {
            setMoney(prev => [...prev, card]);
          }
        });
      }

      // Remove from hand
      setHand(prev => prev.filter(card => !selectedCards.includes(card.id)));

      setMoveMode(false);
      setSelectedCards([]);
      setMoveTarget('');
      setWildPropertyColor('');
    }
  };

  const executeTransfer = () => {
    if (selectedCards.length > 0 && transferTarget) {
      const cardsToTransfer = hand.filter(card => selectedCards.includes(card.id));
      const targetOpponent = opponents.find(opp => opp.id === transferTarget);

      if (!targetOpponent) {
        alert('Invalid opponent selected.');
        return;
      }

      if (transferType === 'properties') {
        // Transfer to opponent's properties
        cardsToTransfer.forEach(card => {
          if (card.type === 'property') {
            let targetColor = card.color || 'other';

            // Handle wild properties - use selected color
            if (targetColor === 'multi' && card.description && card.description.includes('Wild property card')) {
              if (wildPropertyColor) {
                targetColor = wildPropertyColor;
              } else {
                // Fallback to first available color if none selected
                const availableColors = getWildPropertyColors(card);
                targetColor = availableColors[0] || 'other';
              }
            }

            setProperties(prev => ({
              ...prev,
              [targetColor]: [...(prev[targetColor] || []), card]
            }));
          }
        });
      } else if (transferType === 'money') {
        // Transfer to opponent's money pile
        cardsToTransfer.forEach(card => {
          if (card.type === 'money') {
            setMoney(prev => [...prev, card]);
          }
        });
      }

      // Remove from hand
      setHand(prev => prev.filter(card => !selectedCards.includes(card.id)));

      setTransferMode(false);
      setSelectedCards([]);
      setTransferTarget('');
      setTransferType('properties');
      setWildPropertyColor('');
    }
  };

  const moveToHand = (card: Card, type: 'properties' | 'money', color?: string) => {
    if (type === 'properties' && color) {
      setProperties(prev => ({
        ...prev,
        [color]: prev[color]?.filter(c => c.id !== card.id) || []
      }));
    } else if (type === 'money') {
      setMoney(prev => prev.filter(c => c.id !== card.id));
    }

    setHand(prev => [...prev, card]);
  };

  // Add state to prevent multiple simultaneous moves
  const [movingCards, setMovingCards] = useState<Set<string>>(new Set());

  // Opponent transfer functions
  const startOpponentTransfer = (opponentId: number) => {
    setOpponentTransferMode({
      active: true,
      sourceOpponentId: opponentId,
      selectedCards: [],
      targetOpponentId: null,
      targetType: 'properties'
    });
  };

  const cancelOpponentTransfer = () => {
    setOpponentTransferMode({
      active: false,
      sourceOpponentId: null,
      selectedCards: [],
      targetOpponentId: null,
      targetType: 'properties'
    });
  };

  const toggleOpponentCardSelection = (cardId: string, cardType: 'property' | 'money', color?: string, index?: number) => {
    setOpponentTransferMode(prev => {
      const existingIndex = prev.selectedCards.findIndex(c => c.cardId === cardId);
      if (existingIndex >= 0) {
        // Remove from selection
        return {
          ...prev,
          selectedCards: prev.selectedCards.filter(c => c.cardId !== cardId)
        };
      } else {
        // Add to selection
        return {
          ...prev,
          selectedCards: [...prev.selectedCards, { cardId, cardType, color, index: index || 0 }]
        };
      }
    });
  };

  const executeOpponentTransfer = () => {
    if (!opponentTransferMode.sourceOpponentId || !opponentTransferMode.selectedCards.length) return;

    const sourceOpponent = opponents.find(o => o.id === opponentTransferMode.sourceOpponentId);
    if (!sourceOpponent) return;

    // Get the actual cards to transfer
    const cardsToTransfer: Card[] = [];

    opponentTransferMode.selectedCards.forEach(selection => {
      if (selection.cardType === 'property' && selection.color) {
        const card = sourceOpponent.properties?.[selection.color]?.[selection.index];
        if (card) cardsToTransfer.push(card);
      } else if (selection.cardType === 'money') {
        const card = sourceOpponent.money?.[selection.index];
        if (card) cardsToTransfer.push(card);
      }
    });

    // Remove cards from source opponent
    setOpponents(prev => prev.map(opp => {
      if (opp.id !== opponentTransferMode.sourceOpponentId) return opp;

      const newOpp = { ...opp };

      opponentTransferMode.selectedCards.forEach(selection => {
        if (selection.cardType === 'property' && selection.color) {
          newOpp.properties = {
            ...newOpp.properties,
            [selection.color]: newOpp.properties?.[selection.color]?.filter((_, i) => i !== selection.index) || []
          };
        } else if (selection.cardType === 'money') {
          newOpp.money = newOpp.money?.filter((_, i) => i !== selection.index) || [];
        }
      });

      return newOpp;
    }));

    // Add cards to target
    if (opponentTransferMode.targetType === 'hand') {
      // Transfer to user's hand
      setHand(prev => [...prev, ...cardsToTransfer]);
    } else if (opponentTransferMode.targetOpponentId) {
      // Transfer to another opponent
      setOpponents(prev => prev.map(opp => {
        if (opp.id !== opponentTransferMode.targetOpponentId) return opp;

        const newOpp = { ...opp };

        cardsToTransfer.forEach(card => {
          if (opponentTransferMode.targetType === 'properties') {
            const targetColor = card.color || 'brown';
            newOpp.properties = {
              ...newOpp.properties,
              [targetColor]: [...(newOpp.properties?.[targetColor] || []), card]
            };
          } else if (opponentTransferMode.targetType === 'money') {
            newOpp.money = [...(newOpp.money || []), card];
          }
        });

        return newOpp;
      }));
    }

    // Reset transfer mode
    cancelOpponentTransfer();
  };

  // Helper function to return cards to deck (used by opponent cards)
  const returnCardToDeck = (card: Card) => {
    console.log(`Returning ${card.name} to deck`);

    // ULTRA SIMPLE: Just find brown property and increment by 1
    if (card.name === "Brown Property") {
      setDeck((prev: any) => {
        const newDeck = JSON.parse(JSON.stringify(prev)); // Deep copy to avoid mutations

        // Find brown property in deck and increment
        let found = false;
        for (const category of Object.values(newDeck)) {
          for (const deckCard of category as any[]) {
            if (deckCard.id === "brown_prop_1" && !found) {
              deckCard.count++;
              console.log(`✅ Brown Property returned. Count: ${deckCard.count}`);
              found = true;
              break;
            }
          }
          if (found) break;
        }

        if (!found) {
          console.error("Could not find brown_prop_1 in deck!");
        }

        return newDeck;
      });
    } else {
      // Handle other cards
      setDeck((prev: any) => {
        const newDeck = JSON.parse(JSON.stringify(prev));

        const baseCardId = card.id.includes('_') && /\d{13}$/.test(card.id)
          ? card.id.substring(0, card.id.lastIndexOf('_'))
          : card.id;

        let found = false;
        for (const category of Object.values(newDeck)) {
          for (const deckCard of category as any[]) {
            if ((deckCard.id === baseCardId ||
              (deckCard.name === card.name && deckCard.type === card.type)) && !found) {
              deckCard.count++;
              console.log(`✅ ${card.name} returned. Count: ${deckCard.count}`);
              found = true;
              break;
            }
          }
          if (found) break;
        }

        return newDeck;
      });
    }
  };

  const moveToDeck = (card: Card, type: 'hand' | 'properties' | 'money') => {
    // Check if this card is already being moved
    if (movingCards.has(card.id)) {
      console.log(`Preventing duplicate move for ${card.name} - already in progress`);
      return;
    }

    // Mark card as being moved
    setMovingCards(prev => new Set([...prev, card.id]));

    console.log(`Starting move for ${card.name} (ID: ${card.id})`);
    // Remove from source
    if (type === 'hand') {
      setHand(prev => prev.filter(c => c.id !== card.id));
    } else if (type === 'properties') {
      const targetColor = card.color || 'other';
      setProperties(prev => ({
        ...prev,
        [targetColor]: prev[targetColor]?.filter(c => c.id !== card.id) || []
      }));
    } else if (type === 'money') {
      setMoney(prev => prev.filter(c => c.id !== card.id));
    }

    // ULTRA SIMPLE: Just find brown property and increment by 1
    if (card.name === "Brown Property") {
      setDeck((prev: any) => {
        const newDeck = JSON.parse(JSON.stringify(prev)); // Deep copy to avoid mutations

        // Find brown property in deck and increment
        let found = false;
        for (const category of Object.values(newDeck)) {
          for (const deckCard of category as any[]) {
            if (deckCard.id === "brown_prop_1" && !found) {
              deckCard.count++;
              console.log(`✅ Brown Property returned. Count: ${deckCard.count}`);
              found = true;
              break;
            }
          }
          if (found) break;
        }

        if (!found) {
          console.error("Could not find brown_prop_1 in deck!");
        }

        return newDeck;
      });
    } else {
      // Handle other cards
      setDeck((prev: any) => {
        const newDeck = JSON.parse(JSON.stringify(prev));

        const baseCardId = card.id.includes('_') && /\d{13}$/.test(card.id)
          ? card.id.substring(0, card.id.lastIndexOf('_'))
          : card.id;

        let found = false;
        for (const category of Object.values(newDeck)) {
          for (const deckCard of category as any[]) {
            if ((deckCard.id === baseCardId ||
              (deckCard.name === card.name && deckCard.type === card.type)) && !found) {
              deckCard.count++;
              console.log(`✅ ${card.name} returned. Count: ${deckCard.count}`);
              found = true;
              break;
            }
          }
          if (found) break;
        }

        return newDeck;
      });
    }

    // Clear the moving state after a short delay
    setTimeout(() => {
      setMovingCards(prev => {
        const newSet = new Set(prev);
        newSet.delete(card.id);
        return newSet;
      });
    }, 100);
  };

  // NEW: Add opponent property function
  const addOpponentProperty = (opponentId: number, color: string) => {
    // Create a new property card
    const newProperty = {
      id: `${color}_${Date.now()}`,
      name: `${color} Property`,
      type: 'property' as const,
      color: color
    };

    // Add to opponent
    setOpponents((prev: any) => prev.map((p: any) =>
      p.id === opponentId ? {
        ...p,
        properties: {
          ...(p.properties || {}),
          [color]: [...((p.properties || {})[color] || []), newProperty]
        }
      } : p
    ));

    // Reduce deck count
    setDeck((prev: any) => {
      const newDeck = { ...prev };
      Object.values(newDeck).forEach((category: any) => {
        category.forEach((deckCard: any) => {
          if (deckCard.type === 'property' && deckCard.color === color) {
            deckCard.count = Math.max(0, deckCard.count - 1);
          }
        });
      });
      return newDeck;
    });
  };


  // NEW: Handle wild property color selection
  const selectWildPropertyColor = (opponentId: number, _wildType: string, selectedColor: string) => {
    addOpponentProperty(opponentId, selectedColor);
    setWildPropertySelection({
      show: false,
      opponentId: 0,
      wildType: '',
      availableColors: []
    });
  };

  // NEW: Start opponent selection mode
  const startOpponentSelection = (opponentId: number) => {
    setOpponentSelectionMode({
      active: true,
      opponentId: opponentId
    });
  };

  // NEW: Stop opponent selection mode
  const stopOpponentSelection = () => {
    setOpponentSelectionMode({
      active: false,
      opponentId: null
    });
  };

  // NEW: Add card to opponent directly from deck
  const addCardToOpponent = (card: Card) => {
    if (!opponentSelectionMode.active || !opponentSelectionMode.opponentId) return;

    const opponentId = opponentSelectionMode.opponentId;

    // Remove card from deck
    const newDeck = { ...deck };
    Object.values(newDeck).forEach((category: any) => {
      category.forEach((deckCard: any) => {
        if (deckCard.id === card.id && deckCard.count > 0) {
          deckCard.count--;
        }
      });
    });
    setDeck(newDeck);

    // Add to opponent based on card type
    if (card.type === 'property' || (card.type === 'action' && card.color === 'multi')) {
      let targetColor = card.color || 'other';

      // Handle wild properties
      if (targetColor === 'multi' && card.description && card.description.includes('Wild property card')) {
        const availableColors = getWildPropertyColors(card);
        if (availableColors.length > 0) {
          setWildPropertySelection({
            show: true,
            opponentId: opponentId,
            wildType: card.name,
            availableColors: availableColors
          });
          return;
        }
      }

      // Add property to opponent
      const newProperty = {
        id: `${card.id}_${Date.now()}`,
        name: card.name,
        type: 'property' as const,
        color: targetColor,
        value: card.value,
        description: card.description
      };

      setOpponents((prev: any) => prev.map((p: any) =>
        p.id === opponentId ? {
          ...p,
          properties: {
            ...(p.properties || {}),
            [targetColor]: [...((p.properties || {})[targetColor] || []), newProperty]
          }
        } : p
      ));
    } else if (card.type === 'money') {
      const newMoney = {
        id: `${card.id}_${Date.now()}`,
        name: card.name,
        type: 'money' as const,
        value: card.value,
        color: card.color
      };

      setOpponents((prev: any) => prev.map((p: any) =>
        p.id === opponentId ? {
          ...p,
          money: [...(p.money || []), newMoney]
        } : p
      ));
    }
  };

  // Transfer cards from hand to opponents (currently unused but kept for future functionality)
  /*
  const transferToOpponent = (opponentId: number, cardIds: string[], targetType: 'properties' | 'money') => {
    const cardsToTransfer = hand.filter(card => cardIds.includes(card.id));
    
    if (targetType === 'properties') {
      cardsToTransfer.forEach(card => {
        if (card.type === 'property') {
          let targetColor = card.color || 'other';
          
          // Handle wild properties
          if (targetColor === 'multi') {
            // For now, assign to first available color
            targetColor = 'brown'; // Default fallback
          }
          
          setOpponents((prev: any) => prev.map((p: any) => 
            p.id === opponentId ? {
              ...p,
                      properties: {
          ...(p.properties || {}),
          [targetColor]: [...((p.properties || {})[targetColor] || []), card]
        }
            } : p
          ));
        }
      });
    } else if (targetType === 'money') {
      cardsToTransfer.forEach(card => {
        if (card.type === 'money') {
          setOpponents((prev: any) => prev.map((p: any) => 
            p.id === opponentId ? {
              ...p,
              money: [...(p.money || []), card]
            } : p
          ));
        }
      });
    }
    
    // Remove from hand
    setHand(prev => prev.filter(card => !cardIds.includes(card.id)));
  };
  */

  const renderCard = (card: Card, isSelected: boolean = false, onClick?: () => void, showCount: boolean = false) => (
    <div
      key={card.id}
      onClick={onClick}
      className={`
        relative w-20 h-28 rounded-lg border-2 cursor-pointer transition-all duration-200 transform hover:scale-105
        ${isSelected ? 'border-blue-500 shadow-lg scale-105' : 'border-gray-300 hover:border-gray-400'}
        ${getCardColor(card.color || 'gray')}
        text-white shadow-md
      `}
    >
      <div className="p-2 h-full flex flex-col justify-between">
        <div className="text-center">
          <div className="text-xs font-bold mb-1">{card.name}</div>
          {card.value && (
            <div className="text-lg font-bold">${card.value}M</div>
          )}
        </div>

        {card.description && (
          <div className="text-xs text-center opacity-90">
            {card.description}
          </div>
        )}

        {showCount && card.count && card.count > 0 && (
          <div className="absolute -top-2 -right-2 bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold border-2 border-white">
            {card.count}
          </div>
        )}
      </div>
    </div>
  );

  const renderHandTab = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Your Hand</h2>
        <div className="flex gap-2">
          {selectedCards.length > 0 && (
            <>
              <Button onClick={startMove} className="bg-blue-600 hover:bg-blue-700">
                <ArrowRight className="w-4 h-4 mr-2" />
                Move to Piles
              </Button>
              <Button onClick={startTransfer} className="bg-purple-600 hover:bg-purple-700">
                <ArrowRight className="w-4 h-4 mr-2" />
                Transfer to Opponent
              </Button>
            </>
          )}
        </div>
      </div>

      {/* Transfer Controls */}
      {transferMode && (
        <Card className="bg-purple-50 border-purple-200">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <span className="text-purple-800 font-medium">
                {selectedCards.length} card(s) selected for transfer
              </span>

              <div className="flex items-center gap-2">
                <span className="text-purple-800">Transfer to:</span>
                <select
                  value={transferTarget || ''}
                  onChange={(e) => setTransferTarget(Number(e.target.value))}
                  className="border border-purple-300 rounded px-3 py-1"
                >
                  <option value="">Select opponent...</option>
                  {opponents.map(opp => (
                    <option key={opp.id} value={opp.id}>{opp.name}</option>
                  ))}
                </select>

                <span className="text-purple-800">Type:</span>
                <select
                  value={transferType}
                  onChange={(e) => setTransferType(e.target.value as 'properties' | 'money')}
                  className="border border-purple-300 rounded px-3 py-1"
                >
                  <option value="properties">Properties</option>
                  <option value="money">Money</option>
                </select>

                {/* Wild Property Color Selection for Transfer */}
                {transferType === 'properties' && hasWildProperties() && (
                  <div className="flex items-center gap-2">
                    <span className="text-purple-800">Wild property color:</span>
                    <select
                      value={wildPropertyColor}
                      onChange={(e) => setWildPropertyColor(e.target.value)}
                      className="border border-purple-300 rounded px-3 py-1"
                      required
                    >
                      <option value="">Choose color...</option>
                      {(() => {
                        const wildCard = hand.find(c => selectedCards.includes(c.id) && c.color === 'multi');
                        if (wildCard) {
                          const colors = getWildPropertyColors(wildCard);
                          return colors.map(color => (
                            <option key={color} value={color} className="capitalize">
                              {color.replace('-', ' ')}
                            </option>
                          ));
                        }
                        return [];
                      })()}
                    </select>
                  </div>
                )}
              </div>
            </div>

            <div className="flex gap-2 mt-4">
              <Button
                onClick={executeTransfer}
                className="bg-green-600 hover:bg-green-700"
                disabled={!transferTarget || (transferType === 'properties' && hasWildProperties() && !wildPropertyColor)}
              >
                Confirm Transfer
              </Button>
              <Button onClick={cancelTransfer} variant="outline">
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Move Controls */}
      {moveMode && (
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <span className="text-blue-800 font-medium">
                {selectedCards.length} card(s) selected
              </span>

              {moveMode ? (
                <div className="flex items-center gap-2">
                  {/* Show target if auto-determined */}
                  {moveTarget && (
                    <span className="text-blue-800 font-medium">
                      Moving to: <span className="capitalize">{moveTarget}</span>
                    </span>
                  )}

                  {/* Target selection only for mixed cards */}
                  {!moveTarget && (
                    <div className="flex items-center gap-2">
                      <span className="text-blue-800">Mixed cards - choose target:</span>
                      <select
                        value={moveTarget}
                        onChange={(e) => setMoveTarget(e.target.value)}
                        className="border border-blue-300 rounded px-3 py-1"
                      >
                        <option value="">Select target...</option>
                        <option value="properties">Properties</option>
                        <option value="money">Money Pile</option>
                      </select>
                    </div>
                  )}

                  {/* Wild Property Color Selection */}
                  {moveTarget === 'properties' && hasWildProperties() && (
                    <div className="flex items-center gap-2">
                      <span className="text-blue-800">Wild property color:</span>
                      <select
                        value={wildPropertyColor}
                        onChange={(e) => setWildPropertyColor(e.target.value)}
                        className="border border-blue-300 rounded px-3 py-1"
                        required
                      >
                        <option value="">Choose color...</option>
                        {(() => {
                          const wildCard = hand.find(c => selectedCards.includes(c.id) && c.color === 'multi');
                          if (wildCard) {
                            const colors = getWildPropertyColors(wildCard);
                            return colors.map(color => (
                              <option key={color} value={color} className="capitalize">
                                {color.replace('-', ' ')}
                              </option>
                            ));
                          }
                          return [];
                        })()}
                      </select>
                    </div>
                  )}
                </div>
              ) : (
                <Button onClick={startMove} className="bg-blue-600 hover:bg-blue-700">
                  <ArrowRight className="w-4 h-4 mr-2" />
                  Move Cards
                </Button>
              )}

              <div className="flex gap-2">
                {moveMode && (
                  <>
                    <Button
                      onClick={executeMove}
                      className="bg-green-600 hover:bg-green-700"
                      disabled={!moveTarget || (moveTarget === 'properties' && hasWildProperties() && !wildPropertyColor)}
                    >
                      Confirm Move
                    </Button>
                    <Button onClick={cancelMove} variant="outline">
                      Cancel
                    </Button>
                  </>
                )}
                <Button onClick={() => setSelectedCards([])} variant="outline">
                  Clear Selection
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Hand Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {hand.map(card => (
          <div key={card.id} className="relative group">
            {renderCard(
              card,
              selectedCards.includes(card.id),
              () => toggleCardSelection(card.id)
            )}
            {/* Move to deck button - appears on hover */}
            <div className="absolute -top-2 -right-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <Button
                size="sm"
                variant="outline"
                className="h-6 w-6 p-0 bg-white hover:bg-red-50"
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  console.log(`Button clicked for card: ${card.name} (${card.id})`);
                  moveToDeck(card, 'hand');
                }}
                disabled={movingCards.has(card.id)}
                title="Move to Deck"
              >
                <Car className="w-3 h-3" />
              </Button>
            </div>
          </div>
        ))}
        {hand.length === 0 && (
          <div className="col-span-full text-center py-8 text-gray-500">
            <p>Your hand is empty. Draw some cards from the Deck tab!</p>
          </div>
        )}
      </div>
    </div>
  );

  const renderPropertiesTab = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Your Properties</h2>
        <p className="text-gray-600">All properties grouped by color</p>
      </div>

      {Object.keys(properties).length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No properties yet. Move property cards from your hand!</p>
        </div>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>All Properties</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap items-center gap-4">
              {Object.entries(properties).map(([color, propertyCards]) => (
                <div key={color} className="flex items-center">
                  <div className="flex items-center gap-1">
                    {propertyCards.map((card, index) => (
                      <div key={card.id} className="flex items-center group relative">
                        {renderCard(card)}
                        {/* Move back buttons - appear on hover */}
                        <div className="absolute -top-2 -right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                          <Button
                            size="sm"
                            variant="outline"
                            className="h-6 w-6 p-0 bg-white hover:bg-blue-50"
                            onClick={() => moveToHand(card, 'properties', color)}
                            title="Move to Hand"
                          >
                            <Plus className="w-3 h-3" />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            className="h-6 w-6 p-0 bg-white hover:bg-red-50"
                            onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              console.log(`Properties button clicked for: ${card.name} (${card.id})`);
                              moveToDeck(card, 'properties');
                            }}
                            disabled={movingCards.has(card.id)}
                            title="Move to Deck"
                          >
                            <Car className="w-3 h-3" />
                          </Button>
                        </div>
                        {index < propertyCards.length - 1 && (
                          <div className="mx-1 text-gray-400 text-lg font-bold">+</div>
                        )}
                      </div>
                    ))}
                  </div>
                  {Object.keys(properties).indexOf(color) < Object.keys(properties).length - 1 && (
                    <div className="mx-2 text-gray-300 text-xl">|</div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );

  const renderMoneyTab = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Your Money Pile</h2>
        <p className="text-gray-600">Total: ${money.reduce((sum, card) => sum + (card.value || 0), 0)}M</p>
      </div>

      {money.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No money yet. Move money cards from your hand!</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {money.map(card => (
            <div key={card.id} className="relative group">
              {renderCard(card)}
              {/* Move back buttons - appear on hover */}
              <div className="absolute -top-2 -right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                <Button
                  size="sm"
                  variant="outline"
                  className="h-6 w-6 p-0 bg-white hover:bg-blue-50"
                  onClick={() => moveToHand(card, 'money')}
                  title="Move to Hand"
                >
                  <Plus className="w-3 h-3" />
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  className="h-6 w-6 p-0 bg-white hover:bg-red-50"
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log(`Money button clicked for: ${card.name} (${card.id})`);
                    moveToDeck(card, 'money');
                  }}
                  disabled={movingCards.has(card.id)}
                  title="Move to Deck"
                >
                  <Car className="w-3 h-3" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderOpponentsTab = () => {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">Opponent Analysis</h2>
          <Button onClick={() => setOpponents(prev => [...prev, {
            id: Math.max(...prev.map(p => p.id)) + 1,
            name: `Player ${prev.length + 1}`,
            properties: {},
            money: []
          }])}>
            Add Opponent
          </Button>
        </div>

        {opponents.map((opponent) => (
          <Card key={opponent.id} className={opponentSelectionMode.active && opponentSelectionMode.opponentId === opponent.id ? 'ring-2 ring-purple-400 bg-purple-50' : ''}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-3">
                  {opponentSelectionMode.active && opponentSelectionMode.opponentId === opponent.id && (
                    <div className="text-2xl">🎯</div>
                  )}
                  <input
                    type="text"
                    value={opponent.name}
                    onChange={(e) => setOpponents(prev => prev.map(p =>
                      p.id === opponent.id ? { ...p, name: e.target.value } : p
                    ))}
                    className="text-xl font-bold bg-transparent border-b border-transparent hover:border-gray-300 focus:border-blue-500 focus:outline-none px-1"
                  />
                  {opponentSelectionMode.active && opponentSelectionMode.opponentId === opponent.id && (
                    <span className="text-sm text-purple-600 font-normal">(Currently Editing)</span>
                  )}
                </CardTitle>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <div className="text-lg font-bold text-green-600">
                      {Object.values(opponent.properties || {}).reduce((sum: number, props: any[]) => sum + props.length, 0)}
                    </div>
                    <div className="text-gray-600">Properties</div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-blue-600">
                      ${(opponent.money || []).reduce((sum, card) => sum + (card.value || 0), 0)}M
                    </div>
                    <div className="text-gray-600">Total Money</div>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setOpponents(prev => prev.filter(p => p.id !== opponent.id))}
                    disabled={opponents.length <= 1}
                  >
                    Remove
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Opponent Properties */}
                <div>
                  <h3 className="text-lg font-semibold mb-3">Properties</h3>
                  {Object.keys(opponent.properties || {}).length === 0 ? (
                    <div className="text-center py-4 text-gray-500">
                      <p>No properties yet</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {Object.entries(opponent.properties || {}).filter(([, cards]) => cards.length > 0).map(([color, cards]) => (
                        <div key={color} className="p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="capitalize text-sm font-medium">{color.replace('-', ' ')}</span>
                            <span className="text-xs text-gray-500">({cards.length} cards)</span>
                          </div>
                          <div className="flex flex-wrap items-center gap-2">
                            {cards.map((card, index) => {
                              const isSelected = opponentTransferMode.active &&
                                opponentTransferMode.sourceOpponentId === opponent.id &&
                                opponentTransferMode.selectedCards.some(c => c.cardId === card.id);

                              return (
                                <div key={card.id || index} className="flex items-center group relative">
                                  {renderCard(card, isSelected, opponentTransferMode.active && opponentTransferMode.sourceOpponentId === opponent.id ?
                                    () => toggleOpponentCardSelection(card.id, 'property', color, index) : undefined)}
                                  {/* Action buttons - appear on hover */}
                                  <div className="absolute -top-2 -right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                                    <Button
                                      size="sm"
                                      variant="outline"
                                      className="h-6 w-6 p-0 bg-white hover:bg-blue-50"
                                      onClick={() => {
                                        // Move property card to opponent's money pile
                                        const moneyCard = { ...card, type: 'money' as const };
                                        setOpponents(prev => prev.map(p =>
                                          p.id === opponent.id ? {
                                            ...p,
                                            money: [...(p.money || []), moneyCard],
                                            properties: {
                                              ...p.properties,
                                              [color]: p.properties?.[color]?.filter((_, i) => i !== index) || []
                                            }
                                          } : p
                                        ));
                                      }}
                                      title="Move to Money Pile"
                                    >
                                      <Plus className="w-3 h-3" />
                                    </Button>
                                    <Button
                                      size="sm"
                                      variant="outline"
                                      className="h-6 w-6 p-0 bg-white hover:bg-red-50"
                                      onClick={() => {
                                        // Remove from opponent
                                        setOpponents(prev => prev.map(p =>
                                          p.id === opponent.id ? {
                                            ...p,
                                            properties: {
                                              ...p.properties,
                                              [color]: p.properties?.[color]?.filter((_, i) => i !== index) || []
                                            }
                                          } : p
                                        ));
                                        // Add back to deck using helper function
                                        returnCardToDeck(card);
                                      }}
                                      title="Return to Deck"
                                    >
                                      <Car className="w-3 h-3" />
                                    </Button>
                                  </div>
                                  {index < cards.length - 1 && (
                                    <div className="mx-1 text-gray-400 text-lg font-bold">+</div>
                                  )}
                                </div>
                              )
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Opponent selection mode button */}
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      {opponentSelectionMode.active && opponentSelectionMode.opponentId === opponent.id ? (
                        <Button
                          onClick={stopOpponentSelection}
                          className="flex-1 bg-purple-600 hover:bg-purple-700"
                          size="sm"
                        >
                          ✅ Exit Edit Mode
                        </Button>
                      ) : (
                        <Button
                          onClick={() => startOpponentSelection(opponent.id)}
                          className="flex-1 bg-green-600 hover:bg-green-700"
                          size="sm"
                        >
                          🎯 Edit {opponent.name}'s Cards
                        </Button>
                      )}

                      {opponentTransferMode.active && opponentTransferMode.sourceOpponentId === opponent.id ? (
                        <Button
                          onClick={cancelOpponentTransfer}
                          className="flex-1 bg-red-600 hover:bg-red-700"
                          size="sm"
                        >
                          ❌ Cancel Transfer
                        </Button>
                      ) : (
                        <Button
                          onClick={() => startOpponentTransfer(opponent.id)}
                          className="flex-1 bg-blue-600 hover:bg-blue-700"
                          size="sm"
                        >
                          🔄 Transfer Cards
                        </Button>
                      )}
                    </div>
                    <div className="text-xs text-gray-500">
                      {opponentSelectionMode.active && opponentSelectionMode.opponentId === opponent.id ? (
                        <span className="text-purple-600 font-medium">🎯 Currently editing this opponent - go to Deck tab to add cards</span>
                      ) : (
                        <span>💡 Click to enter edit mode, then go to Deck tab and click cards to add them to this opponent</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Opponent Money */}
              <div>
                <h3 className="text-lg font-semibold mb-3">Money</h3>
                {(opponent.money || []).length === 0 ? (
                  <div className="text-center py-4 text-gray-500">
                    <p>No money yet</p>
                  </div>
                ) : (
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium">Money Cards</span>
                        <span className="text-xs text-gray-500">({(opponent.money || []).length} cards)</span>
                      </div>
                      <div className="text-sm font-medium text-green-600">
                        Total: ${(opponent.money || []).reduce((sum, card) => sum + (card.value || 0), 0)}M
                      </div>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                      {(opponent.money || []).map((card, _index) => {
                        const isSelected = opponentTransferMode.active &&
                          opponentTransferMode.sourceOpponentId === opponent.id &&
                          opponentTransferMode.selectedCards.some(c => c.cardId === card.id);

                        return (
                          <div key={card.id || _index} className="flex items-center group relative">
                            {renderCard(card, isSelected, opponentTransferMode.active && opponentTransferMode.sourceOpponentId === opponent.id ?
                              () => toggleOpponentCardSelection(card.id, 'money', undefined, _index) : undefined)}
                            {/* Action buttons - appear on hover */}
                            <div className="absolute -top-2 -right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                              <Button
                                size="sm"
                                variant="outline"
                                className="h-6 w-6 p-0 bg-white hover:bg-blue-50"
                                onClick={() => {
                                  // Move money card to opponent's properties pile (as brown property by default)
                                  const propertyCard = { ...card, type: 'property' as const, color: 'brown' };
                                  setOpponents(prev => prev.map(p =>
                                    p.id === opponent.id ? {
                                      ...p,
                                      properties: {
                                        ...p.properties,
                                        brown: [...(p.properties?.brown || []), propertyCard]
                                      },
                                      money: p.money?.filter((_, i) => i !== _index) || []
                                    } : p
                                  ));
                                }}
                                title="Move to Properties"
                              >
                                <Plus className="w-3 h-3" />
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                className="h-6 w-6 p-0 bg-white hover:bg-red-50"
                                onClick={() => {
                                  // Remove from opponent
                                  setOpponents(prev => prev.map(p =>
                                    p.id === opponent.id ? {
                                      ...p,
                                      money: p.money?.filter((_, i) => i !== _index) || []
                                    } : p
                                  ));
                                  // Add back to deck using helper function
                                  returnCardToDeck(card);
                                }}
                                title="Move to Deck"
                              >
                                <Car className="w-3 h-3" />
                              </Button>
                            </div>
                            {_index < (opponent.money || []).length - 1 && (
                              <div className="mx-1 text-gray-400 text-lg font-bold">+</div>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}

        {/* Transfer Controls */}
        {opponentTransferMode.active && (
          <Card className="bg-blue-50 border-blue-200">
            <CardContent className="pt-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-blue-800 font-medium">
                    Transfer Mode: {opponentTransferMode.selectedCards.length} card(s) selected from {opponents.find(o => o.id === opponentTransferMode.sourceOpponentId)?.name}
                  </span>
                </div>

                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <span className="text-blue-800">Transfer to:</span>
                    <select
                      value={opponentTransferMode.targetType}
                      onChange={(e) => setOpponentTransferMode(prev => ({
                        ...prev,
                        targetType: e.target.value as 'properties' | 'money' | 'hand'
                      }))}
                      className="border border-blue-300 rounded px-3 py-1"
                    >
                      <option value="hand">Your Hand</option>
                      <option value="properties">Opponent Properties</option>
                      <option value="money">Opponent Money</option>
                    </select>
                  </div>

                  {(opponentTransferMode.targetType === 'properties' || opponentTransferMode.targetType === 'money') && (
                    <div className="flex items-center gap-2">
                      <span className="text-blue-800">Target opponent:</span>
                      <select
                        value={opponentTransferMode.targetOpponentId || ''}
                        onChange={(e) => setOpponentTransferMode(prev => ({
                          ...prev,
                          targetOpponentId: Number(e.target.value) || null
                        }))}
                        className="border border-blue-300 rounded px-3 py-1"
                      >
                        <option value="">Select opponent...</option>
                        {opponents.filter(o => o.id !== opponentTransferMode.sourceOpponentId).map(opp => (
                          <option key={opp.id} value={opp.id}>{opp.name}</option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>

                <div className="flex gap-2">
                  <Button
                    onClick={executeOpponentTransfer}
                    className="bg-green-600 hover:bg-green-700"
                    disabled={
                      opponentTransferMode.selectedCards.length === 0 ||
                      (opponentTransferMode.targetType !== 'hand' && !opponentTransferMode.targetOpponentId)
                    }
                  >
                    Confirm Transfer
                  </Button>
                  <Button onClick={cancelOpponentTransfer} variant="outline">
                    Cancel
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* AI Analysis Button */}
        <Card>
          <CardHeader>
            <CardTitle>AI Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-600">
                    {Object.keys(properties).length}
                  </div>
                  <div className="text-gray-600">Your Property Sets</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-green-600">
                    ${money.reduce((sum, card) => sum + (card.value || 0), 0)}M
                  </div>
                  <div className="text-gray-600">Your Money</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-purple-600">
                    {opponents.length}
                  </div>
                  <div className="text-gray-600">Opponents</div>
                </div>
              </div>

              <Button
                className="w-full bg-purple-600 hover:bg-purple-700"
                disabled={analysisLoading}
                onClick={async () => {
                  setAnalysisLoading(true);
                  setAnalysisResult(null);

                  try {
                    // Transform UI state to backend format
                    const players = [
                      // Current player (user)
                      {
                        id: 0,
                        name: "You",
                        hand: hand.map(card => card.name || card.id),
                        bank: money.map(card => card.value || 0),
                        properties: Object.fromEntries(
                          Object.entries(properties).map(([color, cards]) => [
                            color,
                            cards.map(card => card.name || card.id)
                          ])
                        )
                      },
                      // Opponents
                      ...opponents.map((opp, index) => ({
                        id: index + 1,
                        name: opp.name,
                        hand: [], // Opponents' hands are hidden
                        bank: (opp.money || []).map(card => card.value || 0),
                        properties: Object.fromEntries(
                          Object.entries(opp.properties || {}).map(([color, cards]) => [
                            color,
                            cards.map(card => card.name || card.id)
                          ])
                        )
                      }))
                    ];

                    // Calculate total deck count
                    const totalDeckCount = Object.values(deck).reduce((total: number, category: any) => {
                      return total + category.reduce((catTotal: number, card: any) => catTotal + (card.count || 0), 0);
                    }, 0);

                    const gameState = {
                      players,
                      discard: [], // We don't track discard pile in UI yet
                      deckCount: totalDeckCount,
                      edgeRules: edgeRules
                    };

                    console.log('Sending game state to AI:', gameState);

                    // Make API call
                    const response = await fetch('http://localhost:8000/api/v1/analysis/analyze', {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json',
                        // Add auth header if needed
                        // 'Authorization': `Bearer ${token}`
                      },
                      body: JSON.stringify({
                        gameState,
                        strategy: "normal"
                      })
                    });

                    if (!response.ok) {
                      throw new Error(`API call failed: ${response.status} ${response.statusText}`);
                    }

                    const result = await response.json();
                    console.log('AI Analysis Result:', result);

                    // Store results in state
                    setAnalysisResult(result);

                  } catch (error) {
                    console.error('AI Analysis failed:', error);
                    alert(`AI Analysis failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
                  } finally {
                    setAnalysisLoading(false);
                  }
                }}
              >
                {analysisLoading ? '🔄 Analyzing...' : '🧠 Analyze Game State with AI'}
              </Button>

              {/* AI Analysis Results */}
              {analysisResult && (
                <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <h4 className="font-semibold text-green-800 mb-2">🎯 AI Recommendation</h4>
                  <p className="text-green-700 mb-3">{analysisResult.recommendedMove}</p>

                  <h4 className="font-semibold text-green-800 mb-2">💭 Reasoning</h4>
                  <p className="text-green-700 mb-3">{analysisResult.reasoning}</p>

                  <h4 className="font-semibold text-green-800 mb-2">👑 Strongest Player</h4>
                  <p className="text-green-700 mb-3">{analysisResult.strongestPlayer}</p>

                  <h4 className="font-semibold text-green-800 mb-2">📊 Win Probabilities</h4>
                  <div className="space-y-1">
                    {Object.entries(analysisResult.winProbability).map(([player, probability]) => (
                      <div key={player} className="flex justify-between items-center">
                        <span className="text-green-700">{player}:</span>
                        <span className="font-medium text-green-800">{(probability * 100).toFixed(1)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Wild Property Color Selection Modal */}
        {wildPropertySelection.show && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded-xl shadow-xl max-w-md w-full mx-4">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Choose Wild Property Color
              </h3>
              <p className="text-gray-600 mb-4">
                <strong>{wildPropertySelection.wildType}</strong> can be used as either color. Which side do you want to use?
              </p>

              {/* Debug info */}
              <div className="text-xs text-gray-500 mb-2">
                Debug: Available colors: {wildPropertySelection.availableColors.join(', ')}
              </div>

              <div className="grid grid-cols-2 gap-3 mb-6">
                {wildPropertySelection.availableColors.length > 0 ? (
                  wildPropertySelection.availableColors.map((color) => (
                    <Button
                      key={color}
                      className={`h-12 text-sm font-medium text-white ${getCardColor(color)} hover:opacity-80`}
                      onClick={() => selectWildPropertyColor(
                        wildPropertySelection.opponentId,
                        wildPropertySelection.wildType,
                        color
                      )}
                    >
                      {color.replace('-', ' ').toUpperCase()}
                    </Button>
                  ))
                ) : (
                  <div className="col-span-2 text-center text-gray-500 py-4">
                    No colors available. Please try again.
                  </div>
                )}
              </div>

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => setWildPropertySelection({
                    show: false,
                    opponentId: 0,
                    wildType: '',
                    availableColors: []
                  })}
                >
                  Cancel
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderDeckTab = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Card Deck</h2>
        <div className="mb-4">
          <div className="text-3xl font-bold text-blue-600">
            {Object.values(deck).reduce((total: number, category: any) =>
              total + Object.values(category).reduce((sum: number, card: any) => sum + card.count, 0), 0
            )}
          </div>
          <div className="text-sm text-gray-600">Total Cards Remaining</div>
          <Button
            onClick={() => setDeck(JSON.parse(JSON.stringify(COMPLETE_DECK)))}
            variant="outline"
            size="sm"
            className="mt-2"
          >
            Reset Deck to Full
          </Button>
        </div>
        {opponentSelectionMode.active ? (
          <div className="space-y-2">
            <p className="text-purple-600 font-medium">
              🎯 Editing {opponents.find(opp => opp.id === opponentSelectionMode.opponentId)?.name}'s cards
            </p>
            <p className="text-gray-600">Click cards to add them to this opponent</p>
            <Button
              onClick={stopOpponentSelection}
              variant="outline"
              size="sm"
              className="bg-white"
            >
              Exit Edit Mode
            </Button>
          </div>
        ) : (
          <p className="text-gray-600">Click cards to add them to your hand</p>
        )}
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow-sm border text-center">
          <div className="text-2xl font-bold text-blue-600">
            {Object.values(deck.action).reduce((sum: number, card: any) => sum + card.count, 0)}
          </div>
          <div className="text-sm text-gray-600">Action Cards</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border text-center">
          <div className="text-2xl font-bold text-green-600">
            {Object.values(deck.property).reduce((sum: number, card: any) => sum + card.count, 0)}
          </div>
          <div className="text-sm text-gray-600">Properties</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border text-center">
          <div className="text-2xl font-bold text-yellow-600">
            {Object.values(deck.money).reduce((sum: number, card: any) => sum + card.count, 0)}
          </div>
          <div className="text-sm text-gray-600">Money Cards</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border text-center">
          <div className="text-2xl font-bold text-purple-600">
            {Object.values(deck.wildcard).reduce((sum: number, card: any) => sum + card.count, 0) + Object.values(deck.rent).reduce((sum: number, card: any) => sum + card.count, 0)}
          </div>
          <div className="text-sm text-gray-600">Wild/Rent Cards</div>
        </div>
      </div>

      {/* Card Categories with Better Organization */}
      <div className="space-y-8">
        {/* Action Cards */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border border-blue-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-blue-800 flex items-center gap-2">
              ⚡ Action Cards
              <span className="text-sm font-normal text-blue-600">
                ({Object.values(deck.action).reduce((sum: number, card: any) => sum + card.count, 0)} available)
              </span>
            </h3>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {(deck.action as any[]).map((card: any) => (
              <div key={card.id} className="relative group">
                {renderCard(card, false, () => {
                  if (opponentSelectionMode.active) {
                    addCardToOpponent(card);
                  } else {
                    drawCard(card);
                  }
                }, true)}
                {card.count === 0 && (
                  <div className="absolute inset-0 bg-gray-400 bg-opacity-75 rounded-lg flex items-center justify-center">
                    <span className="text-white text-xs font-bold">OUT</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Property Cards */}
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-xl border border-green-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-green-800 flex items-center gap-2">
              🏠 Property Cards
              <span className="text-sm font-normal text-green-600">
                ({Object.values(deck.property).reduce((sum: number, card: any) => sum + card.count, 0)} available)
              </span>
            </h3>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {(deck.property as any[]).map((card: any) => (
              <div key={card.id} className="relative group">
                {renderCard(card, false, () => {
                  if (opponentSelectionMode.active) {
                    addCardToOpponent(card);
                  } else {
                    drawCard(card);
                  }
                }, true)}
                {card.count === 0 && (
                  <div className="absolute inset-0 bg-gray-400 bg-opacity-75 rounded-lg flex items-center justify-center">
                    <span className="text-white text-xs font-bold">OUT</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Money Cards */}
        <div className="bg-gradient-to-r from-yellow-50 to-amber-50 p-6 rounded-xl border border-yellow-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-yellow-800 flex items-center gap-2">
              💰 Money Cards
              <span className="text-sm font-normal text-yellow-600">
                ({Object.values(deck.money).reduce((sum: number, card: any) => sum + card.count, 0)} available)
              </span>
            </h3>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {(deck.money as any[]).map((card: any) => (
              <div key={card.id} className="relative group">
                {renderCard(card, false, () => {
                  if (opponentSelectionMode.active) {
                    addCardToOpponent(card);
                  } else {
                    drawCard(card);
                  }
                }, true)}
                {card.count === 0 && (
                  <div className="absolute inset-0 bg-gray-400 bg-opacity-75 rounded-lg flex items-center justify-center">
                    <span className="text-white text-xs font-bold">OUT</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Wild Card Properties */}
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl border border-purple-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-purple-800 flex items-center gap-2">
              🌈 Wild Property Cards
              <span className="text-sm font-normal text-purple-600">
                ({Object.values(deck.wildcard).reduce((sum: number, card: any) => sum + card.count, 0)} available)
              </span>
            </h3>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {(deck.wildcard as any[]).map((card: any) => (
              <div key={card.id} className="relative group">
                {renderCard(card, false, () => {
                  if (opponentSelectionMode.active) {
                    addCardToOpponent(card);
                  } else {
                    drawCard(card);
                  }
                }, true)}
                {card.count === 0 && (
                  <div className="absolute inset-0 bg-gray-400 bg-opacity-75 rounded-lg flex items-center justify-center">
                    <span className="text-white text-xs font-bold">OUT</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Rent Cards */}
        <div className="bg-gradient-to-r from-orange-50 to-red-50 p-6 rounded-xl border border-orange-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-orange-800 flex items-center gap-2">
              📋 Rent Cards
              <span className="text-sm font-normal text-orange-600">
                ({Object.values(deck.rent).reduce((sum: number, card: any) => sum + card.count, 0)} available)
              </span>
            </h3>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {(deck.rent as any[]).map((card: any) => (
              <div key={card.id} className="relative group">
                {renderCard(card, false, () => {
                  if (opponentSelectionMode.active) {
                    addCardToOpponent(card);
                  } else {
                    drawCard(card);
                  }
                }, true)}
                {card.count === 0 && (
                  <div className="absolute inset-0 bg-gray-400 bg-opacity-75 rounded-lg flex items-center justify-center">
                    <span className="text-white text-xs font-bold">OUT</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Monopoly Deal Card Manager</h1>
          <p className="text-gray-600 text-lg">Manage your deck, hand, properties, and money</p>

          {/* Opponent Edit Mode Indicator */}
          {opponentSelectionMode.active && (
            <div className="mt-4 p-4 bg-purple-100 border-2 border-purple-300 rounded-lg shadow-lg">
              <div className="flex items-center justify-center gap-3">
                <div className="text-2xl">🎯</div>
                <div>
                  <div className="text-lg font-bold text-purple-800">
                    Editing {opponents.find(opp => opp.id === opponentSelectionMode.opponentId)?.name}'s Cards
                  </div>
                  <div className="text-sm text-purple-600">
                    Go to Deck tab and click cards to add them to this opponent
                  </div>
                </div>
                <Button
                  onClick={stopOpponentSelection}
                  variant="outline"
                  size="sm"
                  className="bg-white border-purple-300 text-purple-700 hover:bg-purple-50"
                >
                  Exit Edit Mode
                </Button>
              </div>
            </div>
          )}

          {/* Quick Stats */}
          <div className="mt-4 flex justify-center gap-6 text-sm">
            <div className="bg-white px-4 py-2 rounded-lg shadow-sm border">
              <div className="text-lg font-bold text-blue-600">{hand.length}</div>
              <div className="text-gray-600">Cards in Hand</div>
            </div>
            <div className="bg-white px-4 py-2 rounded-lg shadow-sm border">
              <div className="text-lg font-bold text-green-600">${money.reduce((sum, card) => sum + (card.value || 0), 0)}M</div>
              <div className="text-gray-600">Total Money</div>
            </div>
            <div className="bg-white px-4 py-2 rounded-lg shadow-sm border">
              <div className="text-lg font-bold text-purple-600">{Object.keys(properties).length}</div>
              <div className="text-gray-600">Property Sets</div>
            </div>
            <div className="bg-white px-4 py-2 rounded-lg shadow-sm border">
              <div className="text-lg font-bold text-orange-600">{Object.values(properties).reduce((sum, props) => sum + props.length, 0)}</div>
              <div className="text-gray-600">Total Properties</div>
            </div>
          </div>
        </div>

        {/* Main Tabs - Correct Order: Hand → Properties → Money → Opponents → Deck */}
        <Tabs defaultValue="hand" className="space-y-6">
          <TabsList className="grid w-full grid-cols-6">
            <TabsTrigger value="hand" className="flex items-center gap-2">
              <Plus className="w-4 h-4" />
              Hand ({hand.length})
            </TabsTrigger>
            <TabsTrigger value="properties" className="flex items-center gap-2">
              <Home className="w-4 h-4" />
              Properties
            </TabsTrigger>
            <TabsTrigger value="money" className="flex items-center gap-2">
              <Wallet className="w-4 h-4" />
              Money
            </TabsTrigger>
            <TabsTrigger value="opponents" className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              Opponents
            </TabsTrigger>
            <TabsTrigger value="deck" className={`flex items-center gap-2 ${opponentSelectionMode.active ? 'bg-purple-100 border-purple-300 text-purple-800' : ''}`}>
              <Car className="w-4 h-4" />
              Deck {opponentSelectionMode.active && <span className="text-xs">(Click cards to add to {opponents.find(opp => opp.id === opponentSelectionMode.opponentId)?.name})</span>}
            </TabsTrigger>
            <TabsTrigger value="configuration" className="flex items-center gap-2">
              <Settings className="w-4 h-4" />
              Rules
            </TabsTrigger>
          </TabsList>

          <TabsContent value="hand" className="space-y-6">
            {renderHandTab()}
          </TabsContent>

          <TabsContent value="properties" className="space-y-6">
            {renderPropertiesTab()}
          </TabsContent>

          <TabsContent value="money" className="space-y-6">
            {renderMoneyTab()}
          </TabsContent>

          <TabsContent value="opponents" className="space-y-6">
            {renderOpponentsTab()}
          </TabsContent>

          <TabsContent value="deck" className="space-y-6">
            {renderDeckTab()}
          </TabsContent>

          <TabsContent value="configuration" className="space-y-6">
            <ConfigurationPanel
              currentRules={edgeRules}
              onRulesChange={setEdgeRules}
              onApplyConfiguration={(rules) => {
                setEdgeRules(rules);
                // You can add additional logic here to apply the rules to the game engine
                console.log('Applied configuration:', rules);
              }}
            />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Dashboard;

