import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
// Commented out unused imports to avoid build warnings
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
// import { Switch } from './ui/switch';
import { Label } from './ui/label';

interface EdgeRules {
  housePayment: string;
  hotelMove: string;
  deckExhaustion: string;
  extraProperties: string;
  doubleRentStack: boolean;
  justSayNoOnZero: boolean;
  houseHotelAsPayment: string;
  movingHouseHotel: string;
  deckExhaustionReshuffle: boolean;
  extraPropertiesHandling: string;
  mergingPropertySets: boolean;
  forfeitingBuildings: boolean;
  quadrupleRent: boolean;
  forcedDealToDealBreaker: boolean;
  justSayNoEmptyHand: boolean;
}

interface EdgeCaseConfiguratorProps {
  edgeRules: EdgeRules;
  onEdgeRulesChange: (rules: EdgeRules) => void;
}

export const EdgeCaseConfigurator: React.FC<EdgeCaseConfiguratorProps> = ({
  edgeRules,
  onEdgeRulesChange
}) => {
  const [localRules, setLocalRules] = useState<EdgeRules>(edgeRules);

  const handleRuleChange = (key: keyof EdgeRules, value: string | boolean) => {
    const newRules = { ...localRules, [key]: value };
    setLocalRules(newRules);
  };

  const handleSave = () => {
    onEdgeRulesChange(localRules);
  };

  const handleReset = () => {
    setLocalRules(edgeRules);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Edge Case Configuration</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* House/Hotel Payment Rules */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">House/Hotel Rules</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>House/Hotel as Payment</Label>
                <select 
                  value={localRules.houseHotelAsPayment} 
                  onChange={(e) => handleRuleChange('houseHotelAsPayment', e.target.value)}
                  className="border rounded px-3 py-2"
                >
                  <option value="bank">Go to Bank</option>
                  <option value="incomplete_set">Stay on Incomplete Set</option>
                  <option value="floating">Floating (Can be moved)</option>
                </select>
                <p className="text-xs text-gray-600">
                  Where do House/Hotel cards go when used as payment?
                </p>
              </div>

              <div className="space-y-2">
                <Label>Moving House/Hotel</Label>
                <select 
                  value={localRules.movingHouseHotel} 
                  onChange={(e) => handleRuleChange('movingHouseHotel', e.target.value)}
                  className="border rounded px-3 py-2"
                >
                  <option value="not_allowed">Not Allowed</option>
                  <option value="free_move">Free Move (before rent)</option>
                  <option value="costs_action">Costs 1 Action</option>
                </select>
                <p className="text-xs text-gray-600">
                  Can House/Hotel cards be moved between property sets?
                </p>
              </div>
            </div>
          </div>

          {/* Deck and Game Rules */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Deck & Game Rules</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Deck Exhaustion</Label>
                <select 
                  value={localRules.deckExhaustion} 
                  onChange={(e) => handleRuleChange('deckExhaustion', e.target.value)}
                  className="border rounded px-3 py-2"
                >
                  <option value="reshuffle">Reshuffle Discard Pile</option>
                  <option value="game_over">Game Over</option>
                </select>
                <p className="text-xs text-gray-600">
                  What happens when the deck runs out?
                </p>
              </div>

              <div className="space-y-2">
                <Label>Extra Properties Handling</Label>
                <select 
                  value={localRules.extraPropertiesHandling} 
                  onChange={(e) => handleRuleChange('extraPropertiesHandling', e.target.value)}
                  className="border rounded px-3 py-2"
                >
                  <option value="cap">Cap Rent (Max 3x)</option>
                  <option value="split">Split into Multiple Sets</option>
                </select>
                <p className="text-xs text-gray-600">
                  How are extra properties of the same color handled?
                </p>
              </div>
            </div>
          </div>

          {/* Property Set Rules */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Property Set Rules</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Merging Property Sets</Label>
                <select 
                  value={localRules.mergingPropertySets ? 'true' : 'false'} 
                  onChange={(e) => handleRuleChange('mergingPropertySets', e.target.value === 'true')}
                  className="border rounded px-3 py-2"
                >
                  <option value="true">Allowed</option>
                  <option value="false">Not Allowed</option>
                </select>
                <p className="text-xs text-gray-600">
                  Can orphaned cards combine after wildcard reallocation?
                </p>
              </div>

              <div className="space-y-2">
                <Label>Forfeiting Buildings</Label>
                <select 
                  value={localRules.forfeitingBuildings ? 'true' : 'false'} 
                  onChange={(e) => handleRuleChange('forfeitingBuildings', e.target.value === 'true')}
                  className="border rounded px-3 py-2"
                >
                  <option value="true">Discard Buildings</option>
                  <option value="false">Keep Buildings</option>
                </select>
                <p className="text-xs text-gray-600">
                  Are buildings discarded when sets become incomplete?
                </p>
              </div>
            </div>
          </div>

          {/* Action Card Rules */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Action Card Rules</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Double Rent Stacking</Label>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="doubleRentStack"
                    checked={localRules.doubleRentStack}
                    onChange={(e) => handleRuleChange('doubleRentStack', e.target.checked)}
                    className="rounded"
                  />
                  <Label htmlFor="doubleRentStack">Allow stacking Double Rent cards</Label>
                </div>
                <p className="text-xs text-gray-600">
                  Can multiple Double Rent cards be played together?
                </p>
              </div>

              <div className="space-y-2">
                <Label>Quadruple Rent</Label>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="quadrupleRent"
                    checked={localRules.quadrupleRent}
                    onChange={(e) => handleRuleChange('quadrupleRent', e.target.checked)}
                    className="rounded"
                  />
                  <Label htmlFor="quadrupleRent">Allow quadruple rent</Label>
                </div>
                <p className="text-xs text-gray-600">
                  Can two Double Rent cards be played simultaneously?
                </p>
              </div>

              <div className="space-y-2">
                <Label>Forced Deal → Deal Breaker</Label>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="forcedDealToDealBreaker"
                    checked={localRules.forcedDealToDealBreaker}
                    onChange={(e) => handleRuleChange('forcedDealToDealBreaker', e.target.checked)}
                    className="rounded"
                  />
                  <Label htmlFor="forcedDealToDealBreaker">Valid sequence</Label>
                </div>
                <p className="text-xs text-gray-600">
                  Can Deal Breaker be used to counter Forced Deal?
                </p>
              </div>

              <div className="space-y-2">
                <Label>Just Say No (Empty Hand)</Label>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="justSayNoEmptyHand"
                    checked={localRules.justSayNoEmptyHand}
                    onChange={(e) => handleRuleChange('justSayNoEmptyHand', e.target.checked)}
                    className="rounded"
                  />
                  <Label htmlFor="justSayNoEmptyHand">Allow with no payment ability</Label>
                </div>
                <p className="text-xs text-gray-600">
                  Can Just Say No be used when hand is empty?
                </p>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4 pt-4">
            <Button onClick={handleSave} className="flex-1">
              Save Edge Rules
            </Button>
            <Button onClick={handleReset} variant="outline" className="flex-1">
              Reset to Default
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};



