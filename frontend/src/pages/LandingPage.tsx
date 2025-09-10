import React from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { ArrowRight, Brain, Trophy, Zap, Users, BarChart3, Target, Sparkles, Mail, MessageCircle, Github } from 'lucide-react';

const LandingPage: React.FC = () => {
  const handleGetStarted = () => {
    window.location.href = '/dashboard';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/30 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-40">
        <div className="w-full h-full bg-gradient-to-br from-blue-50/20 to-purple-50/20"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.05),transparent_50%)]"></div>
      </div>
      
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20 relative z-10">
        <div className="text-center max-w-5xl mx-auto">
          <div className="flex justify-center mb-8">
            <div className="relative">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-2xl shadow-2xl">
                <Brain className="w-10 h-10 text-white" />
              </div>
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full animate-pulse"></div>
            </div>
          </div>
          
          <div className="mb-6">
            <div className="inline-flex items-center bg-blue-50 border border-blue-200 rounded-full px-4 py-2 mb-6">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></div>
              <span className="text-blue-700 text-sm font-medium">Research-Backed AI • 45% Win Rate</span>
            </div>
          </div>
          
          <h1 className="text-6xl md:text-7xl font-bold text-slate-900 mb-8 leading-tight">
            Master Property Card Games with
            <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 bg-clip-text text-transparent block mt-2">
              AI-Powered Strategy
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-slate-600 mb-8 leading-relaxed max-w-4xl mx-auto">
            The world's first <strong className="text-slate-800">research-backed AI analyzer</strong> for property card games. 
            Get winning strategies based on peer-reviewed academic research.
          </p>
          
          <div className="flex flex-wrap justify-center gap-6 mb-10 text-sm">
            <div className="flex items-center bg-white/60 backdrop-blur-sm rounded-full px-4 py-2 border border-slate-200">
              <Trophy className="w-4 h-4 text-yellow-500 mr-2" />
              <span className="text-slate-700 font-medium">45% Win Rate Proven</span>
            </div>
            <div className="flex items-center bg-white/60 backdrop-blur-sm rounded-full px-4 py-2 border border-slate-200">
              <Users className="w-4 h-4 text-blue-500 mr-2" />
              <span className="text-slate-700 font-medium">Growing Community</span>
            </div>
            <div className="flex items-center bg-white/60 backdrop-blur-sm rounded-full px-4 py-2 border border-slate-200">
              <Brain className="w-4 h-4 text-purple-500 mr-2" />
              <span className="text-slate-700 font-medium">Academic Research</span>
            </div>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center mb-12">
            <Button 
              onClick={handleGetStarted}
              className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-700 hover:from-blue-700 hover:via-purple-700 hover:to-blue-800 text-white px-10 py-5 text-xl font-bold rounded-2xl shadow-2xl hover:shadow-blue-500/25 transition-all duration-300 transform hover:scale-105 border-0"
            >
              Start Analyzing FREE <ArrowRight className="ml-3 w-6 h-6" />
            </Button>
            <Button 
              variant="outline" 
              className="border-2 border-slate-300 hover:border-slate-400 hover:bg-slate-50 text-slate-700 px-10 py-5 text-xl font-semibold rounded-2xl transition-all duration-300 backdrop-blur-sm"
            >
              <Sparkles className="mr-3 w-5 h-5" />
              Watch Demo
            </Button>
          </div>
          
          <div className="bg-gradient-to-r from-emerald-50 to-blue-50 border-2 border-emerald-200 rounded-xl p-6 inline-block shadow-sm">
            <div className="flex items-center justify-center gap-2 mb-2">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
              <p className="text-emerald-800 font-bold text-lg">
                <strong>Completely Free to Use</strong>
              </p>
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
            </div>
            <p className="text-sm text-emerald-700 text-center">
              No subscriptions • No limits • No catch
            </p>
          </div>
        </div>
      </div>

      {/* Research Credibility Section */}
      <div className="bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Built on Academic Research
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Our AI is based on peer-reviewed research on property card game strategy analysis by researchers at Universitas Pelita Harapan.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Card className="border-2 border-blue-100 hover:border-blue-300 transition-colors duration-300">
              <CardHeader className="text-center">
                <div className="bg-blue-100 p-3 rounded-full w-fit mx-auto mb-4">
                  <Trophy className="w-6 h-6 text-blue-600" />
                </div>
                <CardTitle className="text-blue-900">45% Win Rate</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-600">
                  Aggressive + Logical strategy achieved the highest win rate in academic testing against human players.
                </p>
              </CardContent>
            </Card>
            
            <Card className="border-2 border-purple-100 hover:border-purple-300 transition-colors duration-300">
              <CardHeader className="text-center">
                <div className="bg-purple-100 p-3 rounded-full w-fit mx-auto mb-4">
                  <Brain className="w-6 h-6 text-purple-600" />
                </div>
                <CardTitle className="text-purple-900">BFS Algorithm</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-600">
                  Uses Breadth-First Search decision trees to analyze every possible move and combination.
                </p>
              </CardContent>
            </Card>
            
            <Card className="border-2 border-green-100 hover:border-green-300 transition-colors duration-300">
              <CardHeader className="text-center">
                <div className="bg-green-100 p-3 rounded-full w-fit mx-auto mb-4">
                  <Target className="w-6 h-6 text-green-600" />
                </div>
                <CardTitle className="text-green-900">3 AI Characters</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-600">
                  Aggressive, Defensive, and Normal AI personalities with proven strategic differences.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-gray-50 py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Players Choose Our AI Analyzer
            </h2>
            <p className="text-lg text-gray-600">
              Get the competitive edge with features designed by game theory experts
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
              <Zap className="w-8 h-8 text-yellow-500 mb-4" />
              <h3 className="font-semibold text-gray-900 mb-2">Instant Analysis</h3>
              <p className="text-gray-600 text-sm">Get optimal move recommendations in seconds, not minutes.</p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
              <BarChart3 className="w-8 h-8 text-blue-500 mb-4" />
              <h3 className="font-semibold text-gray-900 mb-2">Win Probability</h3>
              <p className="text-gray-600 text-sm">See your exact chances of winning based on current game state.</p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
              <Users className="w-8 h-8 text-green-500 mb-4" />
              <h3 className="font-semibold text-gray-900 mb-2">Multi-Player Analysis</h3>
              <p className="text-gray-600 text-sm">Analyze complex 2-5 player games with opponent modeling.</p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
              <Sparkles className="w-8 h-8 text-purple-500 mb-4" />
              <h3 className="font-semibold text-gray-900 mb-2">Strategic Insights</h3>
              <p className="text-gray-600 text-sm">Learn why each move is optimal with detailed explanations.</p>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600">
              Three simple steps to master property card games
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="bg-blue-100 text-blue-600 w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Set Up Your Game</h3>
              <p className="text-gray-600">
                Input your cards, properties, and opponent information using our intuitive interface.
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-100 text-purple-600 w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Choose AI Strategy</h3>
              <p className="text-gray-600">
                Select from Aggressive (45% win rate), Defensive, or Normal AI personalities.
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 text-green-600 w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Get Winning Moves</h3>
              <p className="text-gray-600">
                Receive research-backed recommendations with detailed reasoning and win probabilities.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Social Proof / Testimonials */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 py-20 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <div className="w-full h-full bg-[radial-gradient(circle_at_25%_25%,rgba(255,255,255,0.1),transparent_50%),radial-gradient(circle_at_75%_75%,rgba(255,255,255,0.05),transparent_50%)]"></div>
        </div>
        
        <div className="container mx-auto px-4 text-center relative z-10">
          <div className="max-w-3xl mx-auto mb-12">
            <h2 className="text-4xl font-bold mb-6 bg-gradient-to-r from-blue-200 to-purple-200 bg-clip-text text-transparent">
              Join the Community of Strategic Players
            </h2>
            <p className="text-xl text-blue-100 leading-relaxed">
              Players are using our research-backed AI to elevate their property card game strategy
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto mb-12">
            <div className="bg-white/5 backdrop-blur-md border border-white/10 p-8 rounded-2xl hover:bg-white/10 transition-all duration-300">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full flex items-center justify-center text-sm font-bold">
                  SM
                </div>
                <div className="ml-3 text-left">
                  <p className="font-semibold text-white">Sarah M.</p>
                  <p className="text-blue-200 text-sm">Competitive Player</p>
                </div>
              </div>
              <p className="text-blue-100 leading-relaxed">
                "Finally beat my friends consistently! The AI's aggressive strategy is incredible."
              </p>
            </div>
            
            <div className="bg-white/5 backdrop-blur-md border border-white/10 p-8 rounded-2xl hover:bg-white/10 transition-all duration-300">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-gradient-to-r from-green-400 to-blue-400 rounded-full flex items-center justify-center text-sm font-bold">
                  MR
                </div>
                <div className="ml-3 text-left">
                  <p className="font-semibold text-white">Mike R.</p>
                  <p className="text-blue-200 text-sm">Strategy Enthusiast</p>
                </div>
              </div>
              <p className="text-blue-100 leading-relaxed">
                "The research-backed approach gives me confidence in every move I make."
              </p>
            </div>
            
            <div className="bg-white/5 backdrop-blur-md border border-white/10 p-8 rounded-2xl hover:bg-white/10 transition-all duration-300">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full flex items-center justify-center text-sm font-bold">
                  AK
                </div>
                <div className="ml-3 text-left">
                  <p className="font-semibold text-white">Alex K.</p>
                  <p className="text-blue-200 text-sm">Tournament Player</p>
                </div>
              </div>
              <p className="text-blue-100 leading-relaxed">
                "Went from losing most games to winning 60%+ of the time. Game changer!"
              </p>
            </div>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              onClick={handleGetStarted}
              className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white px-8 py-4 text-lg font-semibold rounded-xl shadow-2xl hover:shadow-blue-500/25 transition-all duration-300 border-0"
            >
              Start Winning Today <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
            <Button 
              variant="outline" 
              className="border-2 border-white/20 text-white hover:bg-white/10 px-8 py-4 text-lg font-semibold rounded-xl backdrop-blur-sm transition-all duration-300"
            >
              View Live Demo
            </Button>
          </div>
        </div>
      </div>

      {/* Contact & Footer */}
      <div className="bg-slate-50 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Get in Touch
              </h2>
              <p className="text-lg text-gray-600">
                Have suggestions, feedback, or questions? We'd love to hear from you!
              </p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-8 mb-12">
              <Card className="border-2 border-blue-100 hover:border-blue-300 transition-colors duration-300 hover:shadow-lg">
                <CardContent className="p-6 text-center">
                  <div className="bg-blue-100 p-3 rounded-full w-fit mx-auto mb-4">
                    <Mail className="w-6 h-6 text-blue-600" />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">Email Us</h3>
                  <p className="text-gray-600 mb-3">For suggestions and feedback</p>
                  <a 
                    href="mailto:feedback@monopolydealai.com" 
                    className="text-blue-600 hover:text-blue-800 font-medium transition-colors duration-200"
                  >
                    feedback@monopolydealai.com
                  </a>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-purple-100 hover:border-purple-300 transition-colors duration-300 hover:shadow-lg">
                <CardContent className="p-6 text-center">
                  <div className="bg-purple-100 p-3 rounded-full w-fit mx-auto mb-4">
                    <MessageCircle className="w-6 h-6 text-purple-600" />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">Discord Community</h3>
                  <p className="text-gray-600 mb-3">Join our player community</p>
                  <a 
                    href="#" 
                    className="text-purple-600 hover:text-purple-800 font-medium transition-colors duration-200"
                  >
                    Join Discord
                  </a>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-green-100 hover:border-green-300 transition-colors duration-300 hover:shadow-lg">
                <CardContent className="p-6 text-center">
                  <div className="bg-green-100 p-3 rounded-full w-fit mx-auto mb-4">
                    <Github className="w-6 h-6 text-green-600" />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">Open Source</h3>
                  <p className="text-gray-600 mb-3">Contribute to the project</p>
                  <a 
                    href="#" 
                    className="text-green-600 hover:text-green-800 font-medium transition-colors duration-200"
                  >
                    View on GitHub
                  </a>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-slate-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              <div>
                <div className="flex items-center mb-4">
                  <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-2 rounded-lg mr-3">
                    <Brain className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-xl font-bold">Deal Analyzer Pro</h3>
                </div>
                <p className="text-slate-300 leading-relaxed">
                  The world's first research-backed AI analyzer for property card games. 
                  Built on academic research from Universitas Pelita Harapan.
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold mb-4 text-slate-200">Quick Links</h4>
                <div className="space-y-2">
                  <a href="/dashboard" className="block text-slate-300 hover:text-white transition-colors duration-200">
                    Start Analyzing
                  </a>
                  <a href="#research" className="block text-slate-300 hover:text-white transition-colors duration-200">
                    Research Paper
                  </a>
                  <a href="mailto:feedback@monopolydealai.com" className="block text-slate-300 hover:text-white transition-colors duration-200">
                    Contact Us
                  </a>
                </div>
              </div>
            </div>
            
            <div className="border-t border-slate-700 pt-8 text-center">
              <p className="text-slate-400 mb-2">
                © 2024 Deal Analyzer Pro. Built with research from Universitas Pelita Harapan.
              </p>
              <p className="text-slate-500 text-sm">
                Free forever • No subscriptions • No limits
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;