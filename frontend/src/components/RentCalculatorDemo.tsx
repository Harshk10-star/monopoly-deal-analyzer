import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { 
  calculateTotalRentPotential, 
  calculateRentWithWildCards, 
  formatRentCalculation,
  RENT_VALUES 
} from '../utils/rentCalculator';

export default function RentCalculatorDemo() {
  const [demoProperties, setDemoProperties] = useState({
    'brown': [{ id: 'brown_1', name: 'Brown Property', type: 'property', color: 'brown' }],
    'green': [
      { id: 'green_1', name: 'Green Property', type: 'property', color: 'green' },
      { id: 'green_2', name: 'Green Property', type: 'property', color: 'green' }
    ],
    'dark-blue': [{ id: 'dark_blue_1', name: 'Dark Blue Property', type: 'property', color: 'dark-blue' }]
  });

  // const [demoWildCards, setDemoWildCards] = useState([
  //   { id: 'wild_1', name: 'Purple & Orange Wild', type: 'property', color: 'multi', description: 'Wild property card' }
  // ]);

  const basicRent = calculateTotalRentPotential(demoProperties);
  // Using empty array since demoWildCards is commented out
  const enhancedRent = calculateRentWithWildCards(demoProperties, []);

  const addProperty = (color: string) => {
    setDemoProperties(prev => ({
      ...prev,
      [color]: [...((prev as any)[color] || []), { 
        id: `${color}_${Date.now()}`, 
        name: `${color} Property`, 
        type: 'property', 
        color 
      }]
    }));
  };

  const removeProperty = (color: string) => {
    setDemoProperties(prev => ({
      ...prev,
      [color]: (prev as any)[color]?.slice(0, -1) || []
    }));
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Rent Calculator Demo</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Property Management */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Manage Properties</h3>
              {Object.entries(demoProperties).map(([color, cards]) => (
                <div key={color} className="flex items-center justify-between mb-2 p-2 bg-gray-50 rounded">
                  <span className="capitalize">{color.replace('-', ' ')}: {cards.length} cards</span>
                  <div className="flex gap-1">
                    <Button 
                      size="sm" 
                      onClick={() => addProperty(color)}
                      className="h-6 px-2 text-xs"
                    >
                      +
                    </Button>
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={() => removeProperty(color)}
                      className="h-6 px-2 text-xs"
                      disabled={cards.length === 0}
                    >
                      -
                    </Button>
                  </div>
                </div>
              ))}
            </div>

            {/* Rent Values Reference */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Rent Values Reference</h3>
              <div className="space-y-2 text-sm">
                {Object.entries(RENT_VALUES).map(([color, values]) => (
                  <div key={color} className="flex justify-between">
                    <span className="capitalize">{color.replace('-', ' ')}:</span>
                    <span className="font-mono">
                      {(values as number[]).map((rent: number, i: number) => `${i + 1} card${i > 0 ? 's' : ''}: $${rent}M`).join(' | ')}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Results */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Basic Rent (No Wild Cards)</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600 mb-2">
                  ${basicRent.totalPotentialRent}M
                </div>
                <div className="text-sm text-gray-600">
                  {basicRent.completeSets.length} complete set(s), {basicRent.incompleteSets.length} incomplete set(s)
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Enhanced Rent (With Wild Cards)</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600 mb-2">
                  ${enhancedRent.totalPotentialRent}M
                </div>
                <div className="text-sm text-gray-600">
                  {enhancedRent.completeSets.length} complete set(s), {enhancedRent.incompleteSets.length} incomplete set(s)
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Detailed Breakdown */}
          <div className="mt-4">
            <h3 className="text-lg font-semibold mb-2">Detailed Breakdown</h3>
            <pre className="bg-gray-100 p-3 rounded text-sm overflow-auto">
              {formatRentCalculation(enhancedRent)}
            </pre>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
