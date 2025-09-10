import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Settings, 
  Save, 
  Download, 
  Upload, 
  AlertTriangle, 
  CheckCircle, 
  Info,
  Home,
  Users,
  Zap,
  Shield
} from 'lucide-react';

interface EdgeRules {
  housePayment: 'bank' | 'incomplete_set' | 'floating';
  hotelMove: 'not_allowed' | 'free_move' | 'costs_action';
  deckExhaustion: 'reshuffle' | 'game_over';
  extraProperties: 'cap' | 'split';
  buildingForfeiture: 'discard' | 'to_bank' | 'keep_floating';
  propertyMerging: 'auto_merge' | 'manual_merge' | 'no_merge';
  quadrupleRent: boolean;
  forcedDealToDealBreaker: boolean;
  justSayNoEmptyHand: boolean;
  justSayNoOnZero: boolean;
}

interface ConfigurationPreset {
  id: string;
  name: string;
  description: string;
  rules: EdgeRules;
  is_official: boolean;
  usage_count: number;
}

interface ValidationResult {
  is_valid: boolean;
  errors: string[];
  warnings: string[];
  suggestions: string[];
  performance_impact: 'low' | 'medium' | 'high';
}

interface ConfigurationPanelProps {
  currentRules: EdgeRules;
  onRulesChange: (rules: EdgeRules) => void;
  onApplyConfiguration?: (rules: EdgeRules) => void;
}

const ConfigurationPanel: React.FC<ConfigurationPanelProps> = ({
  currentRules,
  onRulesChange,
  onApplyConfiguration
}) => {
  const [presets, setPresets] = useState<ConfigurationPreset[]>([]);
  const [selectedPreset, setSelectedPreset] = useState<string>('');
  const [customRules, setCustomRules] = useState<EdgeRules>(currentRules);
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [savePresetName, setSavePresetName] = useState('');
  const [savePresetDescription, setSavePresetDescription] = useState('');
  const [showSaveDialog, setShowSaveDialog] = useState(false);

  // Load presets on component mount
  useEffect(() => {
    loadPresets();
  }, []);

  // Validate rules when they change
  useEffect(() => {
    validateConfiguration(customRules);
  }, [customRules]);

  const loadPresets = async () => {
    try {
      const response = await fetch('/api/v1/configuration/presets');
      if (response.ok) {
        const presetsData = await response.json();
        setPresets(presetsData);
      }
    } catch (error) {
      console.error('Failed to load presets:', error);
    }
  };

  const validateConfiguration = async (rules: EdgeRules) => {
    try {
      const response = await fetch('/api/v1/configuration/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(rules)
      });
      
      if (response.ok) {
        const validation = await response.json();
        setValidationResult(validation);
      }
    } catch (error) {
      console.error('Validation failed:', error);
    }
  };

  const handlePresetSelect = (presetId: string) => {
    const preset = presets.find(p => p.id === presetId);
    if (preset) {
      setSelectedPreset(presetId);
      setCustomRules(preset.rules);
      onRulesChange(preset.rules);
    }
  };

  const handleRuleChange = (ruleKey: keyof EdgeRules, value: any) => {
    const newRules = { ...customRules, [ruleKey]: value };
    setCustomRules(newRules);
    onRulesChange(newRules);
    setSelectedPreset(''); // Clear preset selection when customizing
  };

  const handleApplyConfiguration = () => {
    if (onApplyConfiguration) {
      onApplyConfiguration(customRules);
    }
  };

  const handleSavePreset = async () => {
    if (!savePresetName.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('/api/v1/configuration/presets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: savePresetName,
          description: savePresetDescription,
          custom_rules: customRules
        })
      });

      if (response.ok) {
        await loadPresets(); // Reload presets
        setShowSaveDialog(false);
        setSavePresetName('');
        setSavePresetDescription('');
      }
    } catch (error) {
      console.error('Failed to save preset:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExportConfiguration = () => {
    const configData = {
      name: savePresetName || 'Custom Configuration',
      description: savePresetDescription || 'Exported configuration',
      rules: customRules,
      exported_at: new Date().toISOString(),
      version: '1.0'
    };

    const blob = new Blob([JSON.stringify(configData, null, 2)], {
      type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `monopoly-deal-config-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImportConfiguration = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const configData = JSON.parse(e.target?.result as string);
        if (configData.rules) {
          setCustomRules(configData.rules);
          onRulesChange(configData.rules);
          setSelectedPreset('');
        }
      } catch (error) {
        console.error('Failed to import configuration:', error);
      }
    };
    reader.readAsText(file);
  };

  const getPerformanceColor = (impact: string) => {
    switch (impact) {
      case 'low': return 'text-green-600 bg-green-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'high': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getRuleDescription = (ruleKey: string): string => {
    const descriptions: Record<string, string> = {
      housePayment: "How house/hotel cards are handled when received by players without complete sets",
      hotelMove: "Whether house/hotel cards can be moved between property sets",
      deckExhaustion: "What happens when the deck runs out of cards",
      extraProperties: "How extra property cards beyond complete sets are handled",
      buildingForfeiture: "What happens to buildings when property sets become incomplete",
      propertyMerging: "Whether separate property sets of the same color can be merged",
      quadrupleRent: "Whether two 'Double the Rent' cards can be played together",
      forcedDealToDealBreaker: "Whether Forced Deal can be used to set up Deal Breaker combos",
      justSayNoEmptyHand: "Whether 'Just Say No' can be played from an empty hand",
      justSayNoOnZero: "Whether 'Just Say No' can block zero-cost actions"
    };
    return descriptions[ruleKey] || "";
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Settings className="w-5 h-5" />
          Edge Case Configuration
        </CardTitle>
        <p className="text-sm text-gray-600">
          Configure how edge cases and rule ambiguities are handled in your games
        </p>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Preset Selection */}
        <div className="space-y-3">
          <label className="text-sm font-medium">Configuration Presets</label>
          <select
            value={selectedPreset}
            onChange={(e) => handlePresetSelect(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md"
          >
            <option value="">Custom Configuration</option>
            {presets.map(preset => (
              <option key={preset.id} value={preset.id}>
                {preset.name} {preset.is_official ? '(Official)' : ''}
              </option>
            ))}
          </select>
          
          {selectedPreset && (
            <div className="p-3 bg-blue-50 border border-blue-200 rounded-md">
              <p className="text-sm text-blue-800">
                {presets.find(p => p.id === selectedPreset)?.description}
              </p>
            </div>
          )}
        </div>

        {/* Configuration Tabs */}
        <Tabs defaultValue="building" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="building" className="flex items-center gap-1">
              <Home className="w-4 h-4" />
              Building
            </TabsTrigger>
            <TabsTrigger value="property" className="flex items-center gap-1">
              <Users className="w-4 h-4" />
              Property
            </TabsTrigger>
            <TabsTrigger value="action" className="flex items-center gap-1">
              <Zap className="w-4 h-4" />
              Action
            </TabsTrigger>
            <TabsTrigger value="defensive" className="flex items-center gap-1">
              <Shield className="w-4 h-4" />
              Defensive
            </TabsTrigger>
          </TabsList>

          {/* Building Rules Tab */}
          <TabsContent value="building" className="space-y-4">
            <div className="grid gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">House/Hotel Payment Rule</label>
                <p className="text-xs text-gray-500">{getRuleDescription('housePayment')}</p>
                <select
                  value={customRules.housePayment}
                  onChange={(e) => handleRuleChange('housePayment', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  <option value="bank">Goes to Bank (Conservative)</option>
                  <option value="incomplete_set">Can go on Incomplete Sets</option>
                  <option value="floating">Floating Property (Flexible)</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Building Movement Rule</label>
                <p className="text-xs text-gray-500">{getRuleDescription('hotelMove')}</p>
                <select
                  value={customRules.hotelMove}
                  onChange={(e) => handleRuleChange('hotelMove', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  <option value="not_allowed">Not Allowed (Strict)</option>
                  <option value="free_move">Free Movement</option>
                  <option value="costs_action">Costs One Action</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Building Forfeiture Rule</label>
                <p className="text-xs text-gray-500">{getRuleDescription('buildingForfeiture')}</p>
                <select
                  value={customRules.buildingForfeiture}
                  onChange={(e) => handleRuleChange('buildingForfeiture', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  <option value="discard">Discard to Pile</option>
                  <option value="to_bank">Return to Bank</option>
                  <option value="keep_floating">Keep as Floating</option>
                </select>
              </div>
            </div>
          </TabsContent>

          {/* Property Rules Tab */}
          <TabsContent value="property" className="space-y-4">
            <div className="grid gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Extra Properties Rule</label>
                <p className="text-xs text-gray-500">{getRuleDescription('extraProperties')}</p>
                <select
                  value={customRules.extraProperties}
                  onChange={(e) => handleRuleChange('extraProperties', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  <option value="cap">Cap Rent at Maximum</option>
                  <option value="split">Split into Separate Sets</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Property Merging Rule</label>
                <p className="text-xs text-gray-500">{getRuleDescription('propertyMerging')}</p>
                <select
                  value={customRules.propertyMerging}
                  onChange={(e) => handleRuleChange('propertyMerging', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  <option value="auto_merge">Auto-Merge Same Colors</option>
                  <option value="manual_merge">Manual Merge Only</option>
                  <option value="no_merge">No Merging Allowed</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Deck Exhaustion Rule</label>
                <p className="text-xs text-gray-500">{getRuleDescription('deckExhaustion')}</p>
                <select
                  value={customRules.deckExhaustion}
                  onChange={(e) => handleRuleChange('deckExhaustion', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  <option value="reshuffle">Reshuffle Discard Pile</option>
                  <option value="game_over">Game Ends</option>
                </select>
              </div>
            </div>
          </TabsContent>

          {/* Action Rules Tab */}
          <TabsContent value="action" className="space-y-4">
            <div className="grid gap-4">
              <div className="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                <div>
                  <label className="text-sm font-medium">Quadruple Rent</label>
                  <p className="text-xs text-gray-500">{getRuleDescription('quadrupleRent')}</p>
                </div>
                <input
                  type="checkbox"
                  checked={customRules.quadrupleRent}
                  onChange={(e) => handleRuleChange('quadrupleRent', e.target.checked)}
                  className="w-4 h-4"
                />
              </div>

              <div className="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                <div>
                  <label className="text-sm font-medium">Forced Deal → Deal Breaker Combo</label>
                  <p className="text-xs text-gray-500">{getRuleDescription('forcedDealToDealBreaker')}</p>
                </div>
                <input
                  type="checkbox"
                  checked={customRules.forcedDealToDealBreaker}
                  onChange={(e) => handleRuleChange('forcedDealToDealBreaker', e.target.checked)}
                  className="w-4 h-4"
                />
              </div>
            </div>
          </TabsContent>

          {/* Defensive Rules Tab */}
          <TabsContent value="defensive" className="space-y-4">
            <div className="grid gap-4">
              <div className="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                <div>
                  <label className="text-sm font-medium">Just Say No from Empty Hand</label>
                  <p className="text-xs text-gray-500">{getRuleDescription('justSayNoEmptyHand')}</p>
                </div>
                <input
                  type="checkbox"
                  checked={customRules.justSayNoEmptyHand}
                  onChange={(e) => handleRuleChange('justSayNoEmptyHand', e.target.checked)}
                  className="w-4 h-4"
                />
              </div>

              <div className="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                <div>
                  <label className="text-sm font-medium">Just Say No on Zero-Cost Actions</label>
                  <p className="text-xs text-gray-500">{getRuleDescription('justSayNoOnZero')}</p>
                </div>
                <input
                  type="checkbox"
                  checked={customRules.justSayNoOnZero}
                  onChange={(e) => handleRuleChange('justSayNoOnZero', e.target.checked)}
                  className="w-4 h-4"
                />
              </div>
            </div>
          </TabsContent>
        </Tabs>

        {/* Validation Results */}
        {validationResult && (
          <div className="space-y-3">
            <div className={`p-3 rounded-md ${getPerformanceColor(validationResult.performance_impact)}`}>
              <div className="flex items-center gap-2">
                <Info className="w-4 h-4" />
                <span className="text-sm font-medium">
                  Performance Impact: {validationResult.performance_impact.toUpperCase()}
                </span>
              </div>
            </div>

            {validationResult.errors.length > 0 && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-4 h-4 text-red-600" />
                  <span className="text-sm font-medium text-red-800">Errors</span>
                </div>
                <ul className="text-sm text-red-700 space-y-1">
                  {validationResult.errors.map((error, index) => (
                    <li key={index}>• {error}</li>
                  ))}
                </ul>
              </div>
            )}

            {validationResult.warnings.length > 0 && (
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-600" />
                  <span className="text-sm font-medium text-yellow-800">Warnings</span>
                </div>
                <ul className="text-sm text-yellow-700 space-y-1">
                  {validationResult.warnings.map((warning, index) => (
                    <li key={index}>• {warning}</li>
                  ))}
                </ul>
              </div>
            )}

            {validationResult.suggestions.length > 0 && (
              <div className="p-3 bg-blue-50 border border-blue-200 rounded-md">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="w-4 h-4 text-blue-600" />
                  <span className="text-sm font-medium text-blue-800">Suggestions</span>
                </div>
                <ul className="text-sm text-blue-700 space-y-1">
                  {validationResult.suggestions.map((suggestion, index) => (
                    <li key={index}>• {suggestion}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-3 pt-4 border-t">
          <Button onClick={handleApplyConfiguration} className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Apply Configuration
          </Button>
          
          <Button 
            variant="outline" 
            onClick={() => setShowSaveDialog(true)}
            className="flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            Save as Preset
          </Button>
          
          <Button 
            variant="outline" 
            onClick={handleExportConfiguration}
            className="flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            Export
          </Button>
          
          <label className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-md cursor-pointer hover:bg-gray-50">
            <Upload className="w-4 h-4" />
            Import
            <input
              type="file"
              accept=".json"
              onChange={handleImportConfiguration}
              className="hidden"
            />
          </label>
        </div>

        {/* Save Preset Dialog */}
        {showSaveDialog && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded-lg max-w-md w-full mx-4">
              <h3 className="text-lg font-semibold mb-4">Save Configuration Preset</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Preset Name</label>
                  <input
                    type="text"
                    value={savePresetName}
                    onChange={(e) => setSavePresetName(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="My Custom Rules"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Description (Optional)</label>
                  <textarea
                    value={savePresetDescription}
                    onChange={(e) => setSavePresetDescription(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    rows={3}
                    placeholder="Describe your configuration..."
                  />
                </div>
              </div>
              
              <div className="flex gap-3 mt-6">
                <Button 
                  onClick={handleSavePreset} 
                  disabled={!savePresetName.trim() || loading}
                  className="flex-1"
                >
                  {loading ? 'Saving...' : 'Save Preset'}
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => setShowSaveDialog(false)}
                  className="flex-1"
                >
                  Cancel
                </Button>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ConfigurationPanel;