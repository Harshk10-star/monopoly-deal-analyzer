import React from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

// Complete card data with proper counts
const CARD_LIBRARY = {
  action: [
    { name: "Deal Breaker", count: 2, color: "red", description: "Steal a complete property set" },
    { name: "Just Say No", count: 3, color: "blue", description: "Cancel any action card" },
    { name: "Sly Deal", count: 3, color: "purple", description: "Steal a property from any player" },
    { name: "Force Deal", count: 4, color: "orange", description: "Swap a property with any player" },
    { name: "Debt Collector", count: 3, color: "yellow", description: "Take $5M from any player" },
    { name: "It's My Birthday", count: 3, color: "pink", description: "All players give you $2M" },
    { name: "Pass Go", count: 10, color: "green", description: "Draw 2 cards" },
    { name: "House", count: 3, color: "brown", description: "Add to a complete property set" },
    { name: "Hotel", count: 3, color: "brown", description: "Add to a complete property set" },
    { name: "Double The Rent", count: 2, color: "gold", description: "Double the rent you collect" }
  ],
  property: [
    { name: "Brown Property", count: 2, color: "brown", value: 1 },
    { name: "Light Blue Property", count: 3, color: "light-blue", value: 1 },
    { name: "Pink Property", count: 3, color: "pink", value: 2 },
    { name: "Orange Property", count: 3, color: "orange", value: 2 },
    { name: "Red Property", count: 3, color: "red", value: 3 },
    { name: "Yellow Property", count: 3, color: "yellow", value: 3 },
    { name: "Green Property", count: 3, color: "green", value: 4 },
    { name: "Dark Blue Property", count: 2, color: "dark-blue", value: 4 },
    { name: "Railroad Property", count: 4, color: "black", value: 2 },
    { name: "Utility Property", count: 2, color: "gray", value: 1 }
  ],
  money: [
    { name: "$1M", count: 6, value: 1, color: "green" },
    { name: "$2M", count: 5, value: 2, color: "blue" },
    { name: "$3M", count: 3, value: 3, color: "red" },
    { name: "$4M", count: 3, value: 4, color: "purple" },
    { name: "$5M", count: 2, value: 5, color: "orange" },
    { name: "$10M", count: 1, value: 10, color: "gold" }
  ],
  wildcard: [
    { name: "Purple & Orange", count: 2, color: "multi", description: "Wild property card" },
    { name: "Light Blue & Brown", count: 1, color: "multi", description: "Wild property card" },
    { name: "Light Blue & Railroad", count: 1, color: "multi", description: "Wild property card" },
    { name: "Dark Blue & Green", count: 1, color: "multi", description: "Wild property card" },
    { name: "Railroad & Green", count: 1, color: "multi", description: "Wild property card" },
    { name: "Red & Yellow", count: 2, color: "multi", description: "Wild property card" },
    { name: "Utility & Railroad", count: 1, color: "multi", description: "Wild property card" },
    { name: "10-Color Wild", count: 2, color: "multi", description: "Wild property card" }
  ],
  rent: [
    { name: "Purple & Orange Rent", count: 2, color: "multi", description: "Collect rent from purple or orange properties" },
    { name: "Railroad & Utility Rent", count: 2, color: "multi", description: "Collect rent from railroad or utility properties" },
    { name: "Green & Dark Blue Rent", count: 2, color: "multi", description: "Collect rent from green or dark blue properties" },
    { name: "Brown & Light Blue Rent", count: 2, color: "multi", description: "Collect rent from brown or light blue properties" },
    { name: "Red & Yellow Rent", count: 2, color: "multi", description: "Collect rent from red or yellow properties" },
    { name: "All Color Wild Rent", count: 3, color: "multi", description: "Collect rent from any color properties" }
  ]
};

const CardLibrary: React.FC = () => {
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
      'black': 'bg-gray-800',
      'gray': 'bg-gray-500',
      'blue': 'bg-blue-600',
      'purple': 'bg-purple-600',
      'gold': 'bg-yellow-400',
      'multi': 'bg-gradient-to-r from-purple-400 to-pink-400'
    };
    return colorMap[color] || 'bg-gray-400';
  };

  const renderCard = (card: any) => (
    <div
      key={card.name}
      className={`
        relative w-24 h-32 rounded-lg border-2 transition-all duration-200 transform hover:scale-105
        ${getCardColor(card.color)}
        text-white shadow-lg
      `}
    >
      <div className="p-2 h-full flex flex-col justify-between">
        <div className="text-center">
          <div className="text-xs font-bold mb-1 leading-tight">{card.name}</div>
          {card.value && (
            <div className="text-lg font-bold">${card.value}M</div>
          )}
        </div>
        
        {card.description && (
          <div className="text-xs text-center opacity-90 leading-tight">
            {card.description}
          </div>
        )}
        
        {/* Card count indicator */}
        <div className="absolute -top-2 -right-2 bg-white text-gray-800 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold border-2 border-gray-300">
          {card.count}
        </div>
      </div>
    </div>
  );

  const getTotalCards = (category: string) => {
    return CARD_LIBRARY[category as keyof typeof CARD_LIBRARY]?.reduce((sum, card) => sum + card.count, 0) || 0;
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Monopoly Deal Card Library</h2>
        <p className="text-gray-600">Complete reference of all cards in the deck</p>
      </div>

      <Tabs defaultValue="action" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="action">Action ({getTotalCards('action')})</TabsTrigger>
          <TabsTrigger value="property">Property ({getTotalCards('property')})</TabsTrigger>
          <TabsTrigger value="money">Money ({getTotalCards('money')})</TabsTrigger>
          <TabsTrigger value="wildcard">Wildcards ({getTotalCards('wildcard')})</TabsTrigger>
          <TabsTrigger value="rent">Rent ({getTotalCards('rent')})</TabsTrigger>
        </TabsList>

        {Object.entries(CARD_LIBRARY).map(([category, cards]) => (
          <TabsContent key={category} value={category} className="space-y-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-800 mb-2 capitalize">
                {category} Cards - {getTotalCards(category)} total
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {cards.map(card => renderCard(card))}
              </div>
            </div>
          </TabsContent>
        ))}
      </Tabs>

      <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-800 mb-2">Deck Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {Object.values(CARD_LIBRARY).flat().reduce((sum, card) => sum + card.count, 0)}
            </div>
            <div className="text-blue-800">Total Cards</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {CARD_LIBRARY.money.reduce((sum, card) => sum + (card.value * card.count), 0)}
            </div>
            <div className="text-green-800">Total Money</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">
              {CARD_LIBRARY.property.length}
            </div>
            <div className="text-purple-800">Property Types</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">
              {CARD_LIBRARY.action.length}
            </div>
            <div className="text-orange-800">Action Types</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CardLibrary;
