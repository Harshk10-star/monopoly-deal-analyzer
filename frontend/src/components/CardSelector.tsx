import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
// import { Checkbox } from './ui/checkbox';
import { api } from '../services/api';

interface Card {
  id: string;
  name: string;
  type: 'property' | 'money' | 'action' | 'building';
  color?: string;
  value?: number;
  description?: string;
}

interface Player {
  id: number;
  name: string;
  hand: Card[];
  bank: number[];
  properties: { [color: string]: Card[] };
}

interface CardSelectorProps {
  currentPlayer: Player;
  opponents: Player[];
  onCardOperation: (operation: any) => void;
  edgeRules: any;
}

export const CardSelector: React.FC<CardSelectorProps> = ({
  currentPlayer,
  opponents,
  onCardOperation,
  edgeRules
}) => {
  const [selectedCards, setSelectedCards] = useState<string[]>([]);
  const [targetLocation, setTargetLocation] = useState<string>('properties');
  const [targetPropertySet, setTargetPropertySet] = useState<string>('');
  const [targetPlayerId, setTargetPlayerId] = useState<number | null>(null);
  const [operationType, setOperationType] = useState<'transfer' | 'play' | 'discard'>('transfer');

  const propertyColors = [
    'brown', 'light_blue', 'dark_blue', 'green', 'red', 
    'yellow', 'orange', 'pink', 'railroad', 'utility'
  ];

  const handleCardToggle = (cardId: string) => {
    setSelectedCards(prev => 
      prev.includes(cardId) 
        ? prev.filter(id => id !== cardId)
        : [...prev, cardId]
    );
  };

  const handleTransfer = async () => {
    if (selectedCards.length === 0) return;

    const operation = {
      selectedCards,
      action: operationType,
      targetLocation,
      targetPlayerId: targetPlayerId || currentPlayer.id,
      propertySet: targetPropertySet
    };

    try {
      const response = await api.post('/api/v1/analysis/card-operation', {
        gameState: {
          players: [currentPlayer, ...opponents],
          discard: [],
          deckCount: 0,
          edgeRules
        },
        operation
      });

      if (response.data.success) {
        onCardOperation(response.data.newGameState);
        setSelectedCards([]);
        setTargetLocation('properties');
        setTargetPropertySet('');
        setTargetPlayerId(null);
      }
    } catch (error) {
      console.error('Card operation failed:', error);
    }
  };

  const canTransferToProperties = selectedCards.length > 0 && targetPropertySet;
  const canTransferToBank = selectedCards.length > 0 && targetLocation === 'bank';
  const canTransferToOpponent = selectedCards.length > 0 && targetPlayerId && targetPlayerId !== currentPlayer.id;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Card Selection & Transfer</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Operation Type Selection */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Operation Type</label>
            <select value={operationType} onChange={(e) => setOperationType(e.target.value as any)} className="border rounded px-3 py-2">
              <option value="transfer">Transfer Cards</option>
              <option value="play">Play Cards</option>
              <option value="discard">Discard Cards</option>
            </select>
          </div>

          {/* Target Location Selection */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Target Location</label>
            <select value={targetLocation} onChange={(e) => setTargetLocation(e.target.value)} className="border rounded px-3 py-2">
              <option value="properties">Properties</option>
              <option value="bank">Bank (Money)</option>
              <option value="discard">Discard Pile</option>
              <option value="opponent">Opponent</option>
            </select>
          </div>

          {/* Property Set Selection (for property transfers) */}
          {targetLocation === 'properties' && (
            <div className="space-y-2">
              <label className="text-sm font-medium">Property Set</label>
              <select value={targetPropertySet} onChange={(e) => setTargetPropertySet(e.target.value)} className="border rounded px-3 py-2">
                <option value="">Select property set</option>
                {propertyColors.map(color => (
                  <option key={color} value={color}>
                    {color.replace('_', ' ').toUpperCase()}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Opponent Selection (for opponent transfers) */}
          {targetLocation === 'opponent' && (
            <div className="space-y-2">
              <label className="text-sm font-medium">Target Opponent</label>
              <select value={targetPlayerId?.toString() || ''} onChange={(e) => setTargetPlayerId(parseInt(e.target.value))} className="border rounded px-3 py-2">
                <option value="">Select opponent</option>
                {opponents.map(opponent => (
                  <option key={opponent.id} value={opponent.id.toString()}>
                    {opponent.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Current Player's Hand */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Select Cards from Hand</label>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
              {currentPlayer.hand.map(card => (
                <div
                  key={card.id}
                  className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                    selectedCards.includes(card.id)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleCardToggle(card.id)}
                >
                  <div className="text-sm font-medium">{card.name}</div>
                  {card.color && (
                    <Badge variant="secondary" className="text-xs mt-1">
                      {card.color}
                    </Badge>
                  )}
                  {card.value && (
                    <div className="text-xs text-gray-600 mt-1">${card.value}M</div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Transfer Button */}
          <Button
            onClick={handleTransfer}
            disabled={!canTransferToProperties && !canTransferToBank && !canTransferToOpponent}
            className="w-full"
          >
            {operationType === 'transfer' ? 'Transfer Selected Cards' : 
             operationType === 'play' ? 'Play Selected Cards' : 'Discard Selected Cards'}
          </Button>

          {/* Edge Rules Display */}
          <div className="mt-4 p-3 bg-gray-50 rounded-lg">
            <h4 className="text-sm font-medium mb-2">Current Edge Rules</h4>
            <div className="text-xs text-gray-600 space-y-1">
              <div>House/Hotel as Payment: {edgeRules.houseHotelAsPayment}</div>
              <div>Moving House/Hotel: {edgeRules.movingHouseHotel}</div>
              <div>Deck Exhaustion: {edgeRules.deckExhaustionReshuffle ? 'Reshuffle' : 'Game Over'}</div>
              <div>Extra Properties: {edgeRules.extraPropertiesHandling}</div>
              <div>Quadruple Rent: {edgeRules.quadrupleRent ? 'Allowed' : 'Not Allowed'}</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};



