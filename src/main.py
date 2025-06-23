import pygame
import random
import time
import sys
import math

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Configurações da janela
LARGURA = 1000
ALTURA = 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🌌 Guia do Mochileiro das Galáxias - Gerador de Improbabilidade Infinita")

# Cores modernas com gradientes
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE_NEON = (57, 255, 20)
VERDE_ESCURO = (0, 100, 0)
VERMELHO_NEON = (255, 20, 60)
AZUL_CYBER = (0, 255, 255)
ROXO_ESPACIAL = (138, 43, 226)
AMARELO_OURO = (255, 215, 0)
LARANJA_NEON = (255, 165, 0)
ROSA_NEON = (255, 20, 147)
CINZA_ESCURO = (30, 30, 30)
CINZA_MEDIO = (80, 80, 80)

# Fontes modernas
try:
    fonte_titulo_grande = pygame.font.Font(None, 48)
    fonte_titulo = pygame.font.Font(None, 36)
    fonte_texto = pygame.font.Font(None, 24)
    fonte_pequena = pygame.font.Font(None, 18)
    fonte_gigante = pygame.font.Font(None, 96)
except:
    fonte_titulo_grande = pygame.font.Font(None, 48)
    fonte_titulo = pygame.font.Font(None, 36)
    fonte_texto = pygame.font.Font(None, 24)
    fonte_pequena = pygame.font.Font(None, 18)
    fonte_gigante = pygame.font.Font(None, 96)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.stars = []
        self.init_stars()
    
    def init_stars(self):
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, LARGURA),
                'y': random.randint(0, ALTURA),
                'speed': random.uniform(0.1, 0.5),
                'brightness': random.randint(100, 255)
            })
    
    def add_particle(self, x, y, color, life=60):
        self.particles.append({
            'x': x,
            'y': y,
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-2, 2),
            'color': color,
            'life': life,
            'max_life': life
        })
    
    def update_and_draw(self, surface):
        # Desenhar estrelas em movimento
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > ALTURA:
                star['y'] = 0
                star['x'] = random.randint(0, LARGURA)
            
            alpha = star['brightness']
            color = (alpha, alpha, alpha)
            pygame.draw.circle(surface, color, (int(star['x']), int(star['y'])), 1)
        
        # Atualizar partículas
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
            else:
                alpha = int(255 * (particle['life'] / particle['max_life']))
                color = (*particle['color'][:3], alpha)
                size = max(1, int(3 * (particle['life'] / particle['max_life'])))
                pygame.draw.circle(surface, color[:3], (int(particle['x']), int(particle['y'])), size)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BRANCO):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.animation_scale = 1.0
        self.glow_intensity = 0
        self.click_animation = 0
        self.ripple_effect = 0
    
    def update(self, mouse_pos):
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Hover sound effect simulation (visual feedback)
        if self.is_hovered and not was_hovered:
            self.ripple_effect = 30
        
        # Smooth animations
        target_scale = 1.1 if self.is_hovered else 1.0
        self.animation_scale += (target_scale - self.animation_scale) * 0.15
        
        # Glow effect
        target_glow = 25 if self.is_hovered else 0
        self.glow_intensity += (target_glow - self.glow_intensity) * 0.12
        
        # Update effects
        if self.click_animation > 0:
            self.click_animation -= 2
        if self.ripple_effect > 0:
            self.ripple_effect -= 1
    
    def draw(self, surface):
        # Calculate animated rectangle
        center = self.rect.center
        click_scale = 1.0 - (self.click_animation * 0.01)
        total_scale = self.animation_scale * click_scale
        
        new_width = int(self.rect.width * total_scale)
        new_height = int(self.rect.height * total_scale)
        animated_rect = pygame.Rect(0, 0, new_width, new_height)
        animated_rect.center = center
        
        # Draw ripple effect
        if self.ripple_effect > 0:
            ripple_radius = (30 - self.ripple_effect) * 3
            ripple_alpha = self.ripple_effect * 8
            ripple_color = (*self.hover_color[:3], min(255, ripple_alpha))
            pygame.draw.circle(surface, self.hover_color, center, ripple_radius, 2)
        
        # Draw glow
        if self.glow_intensity > 0:
            for i in range(3):
                glow_rect = animated_rect.inflate(int(self.glow_intensity - i*3), int(self.glow_intensity - i*3))
                glow_alpha = max(0, int(self.glow_intensity - i*10))
                glow_color = (*self.hover_color[:3], glow_alpha)
                pygame.draw.rect(surface, self.hover_color, glow_rect, border_radius=15, width=1)
        
        # Draw button background with gradient effect
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, animated_rect, border_radius=15)
        
        # Add inner highlight for 3D effect
        if self.is_hovered:
            highlight_rect = animated_rect.inflate(-4, -4)
            highlight_color = tuple(min(255, c + 30) for c in color[:3])
            pygame.draw.rect(surface, highlight_color, highlight_rect, border_radius=12, width=2)
        
        # Draw border
        border_color = AMARELO_OURO if self.is_hovered else BRANCO
        pygame.draw.rect(surface, border_color, animated_rect, 2, border_radius=15)
        
        # Draw text with shadow for better readability
        shadow_surface = fonte_texto.render(self.text, True, PRETO)
        shadow_rect = shadow_surface.get_rect(center=(animated_rect.centerx + 1, animated_rect.centery + 1))
        surface.blit(shadow_surface, shadow_rect)
        
        text_surface = fonte_texto.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=animated_rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        if self.rect.collidepoint(mouse_pos) and mouse_clicked:
            self.click_animation = 20  # Trigger click animation
            return True
        return False

class JogoAdivinhacao:
    def __init__(self):
        self.numero_secreto = round(random.random() * 100)
        self.estado = "introducao"
        self.tempo_inicial = time.time()
        self.mensagem_atual = 0
        self.tentativas = 0
        self.tentativa_bonus = 0
        self.chute = ""
        self.historico_chutes = []
        self.contador_timer = 5
        self.tempo_timer = 0
        self.particles = ParticleSystem()
        self.typing_effect_index = 0
        self.typing_timer = 0
        self.glitch_effect = 0
        self.pulse_effect = 0
        self.input_blink = 0
        self.chute_atual = 0  # Added missing attribute
        
        # Botões
        self.restart_button = Button(LARGURA//2 - 100, 500, 200, 50, "JOGAR NOVAMENTE", VERDE_ESCURO, VERDE_NEON)
        self.quit_button = Button(LARGURA//2 - 100, 560, 200, 50, "SAIR", VERMELHO_NEON, ROSA_NEON)
        
        # Mensagens de introdução com efeitos especiais
        self.mensagens_intro = [
            {"texto": "Bem vindo ao jogo de adivinhação!", "cor": AZUL_CYBER, "efeito": "normal"},
            {"texto": "NÃO ENTRE EM PÂNICO!!!", "cor": VERMELHO_NEON, "efeito": "glitch"},
            {"texto": "Trabalhando no gerador de improbabilidade infinita...", "cor": VERDE_NEON, "efeito": "typing"},
            {"texto": "Prepare-se...", "cor": AMARELO_OURO, "efeito": "pulse"},
            {"texto": "Pergunta...", "cor": LARANJA_NEON, "efeito": "fade"},
            {"texto": "Qual é a resposta para a vida, o universo e tudo mais?", "cor": ROXO_ESPACIAL, "efeito": "rainbow"},
            {"texto": "Ajustando o gerador de improbabilidade infinita...", "cor": AZUL_CYBER, "efeito": "wave"},
            {"texto": "A resposta está entre 0 e 100", "cor": BRANCO, "efeito": "normal"},
            {"texto": "Pense na sua resposta... O tempo está acabando...", "cor": VERMELHO_NEON, "efeito": "pulse"}
        ]
        
        self.tempo_mensagens = [3, 3, 3, 3, 3, 3, 3, 1, 0]
        self.tempo_proxima_mensagem = time.time() + self.tempo_mensagens[0]
    
    def draw_gradient_background(self, surface):
        """Desenha um fundo com gradiente espacial"""
        for y in range(ALTURA):
            ratio = y / ALTURA
            r = int(10 * (1 - ratio))
            g = int(5 * (1 - ratio))
            b = int(25 + 30 * ratio)
            color = (r, g, b)
            pygame.draw.line(surface, color, (0, y), (LARGURA, y))
    
    def draw_text_with_effect(self, surface, texto, x, y, cor, efeito="normal", fonte=None):
        """Desenha texto com efeitos especiais"""
        if fonte is None:
            fonte = fonte_texto
        
        current_time = time.time()
        
        if efeito == "glitch":
            # Efeito glitch
            offset_x = random.randint(-2, 2) if random.random() < 0.1 else 0
            offset_y = random.randint(-1, 1) if random.random() < 0.1 else 0
            
            # Desenhar sombras coloridas
            shadow_colors = [VERMELHO_NEON, AZUL_CYBER, VERDE_NEON]
            for i, shadow_color in enumerate(shadow_colors):
                shadow_surface = fonte.render(texto, True, shadow_color)
                shadow_rect = shadow_surface.get_rect(center=(x + offset_x + i, y + offset_y + i))
                surface.blit(shadow_surface, shadow_rect)
        
        elif efeito == "pulse":
            # Efeito pulsante
            scale = 1 + 0.2 * math.sin(current_time * 8)
            pulse_font_size = int(fonte.get_height() * scale)
            try:
                pulse_font = pygame.font.Font(None, pulse_font_size)
                texto_surface = pulse_font.render(texto, True, cor)
            except:
                texto_surface = fonte.render(texto, True, cor)
        
        elif efeito == "wave":
            # Efeito ondulante
            for i, char in enumerate(texto):
                char_surface = fonte.render(char, True, cor)
                char_x = x + i * fonte.get_height() * 0.6 - len(texto) * fonte.get_height() * 0.3
                char_y = y + math.sin(current_time * 5 + i * 0.5) * 5
                surface.blit(char_surface, (char_x, char_y))
            return
        
        elif efeito == "rainbow":
            # Efeito arco-íris
            colors = [VERMELHO_NEON, LARANJA_NEON, AMARELO_OURO, VERDE_NEON, AZUL_CYBER, ROXO_ESPACIAL]
            color_index = int(current_time * 2) % len(colors)
            cor = colors[color_index]
        
        # Desenhar texto principal
        if efeito != "wave":
            texto_surface = fonte.render(texto, True, cor)
            texto_rect = texto_surface.get_rect(center=(x, y))
            surface.blit(texto_surface, texto_rect)
    
    def draw_input_field(self, surface):
        """Enhanced futuristic input field with better UX"""
        # Main field
        field_rect = pygame.Rect(LARGURA//2 - 200, 300, 400, 60)
        
        # Animated glow with validation feedback
        is_valid = self.chute.isdigit() and 0 <= int(self.chute) <= 100 if self.chute else True
        glow_color = VERDE_NEON if is_valid and self.chute else AZUL_CYBER
        if not is_valid:
            glow_color = VERMELHO_NEON
        
        glow_intensity = int(20 + 10 * math.sin(time.time() * 3))
        for i in range(3):
            glow_rect = field_rect.inflate(i*4, i*4)
            pygame.draw.rect(surface, glow_color, glow_rect, border_radius=15, width=1)
        
        # Field background with gradient
        pygame.draw.rect(surface, CINZA_ESCURO, field_rect, border_radius=15)
        
        # Inner highlight for depth
        inner_rect = field_rect.inflate(-6, -6)
        pygame.draw.rect(surface, (50, 50, 50), inner_rect, border_radius=12)
        
        # Border with validation color
        border_color = glow_color
        pygame.draw.rect(surface, border_color, field_rect, 3, border_radius=15)
        
        # Placeholder text when empty
        if not self.chute:
            placeholder_surface = fonte_texto.render("Digite um número (0-100)", True, CINZA_MEDIO)
            placeholder_rect = placeholder_surface.get_rect(center=field_rect.center)
            surface.blit(placeholder_surface, placeholder_rect)
        else:
            # Typed text with better positioning
            text_surface = fonte_titulo.render(self.chute, True, BRANCO)
            text_rect = text_surface.get_rect(center=field_rect.center)
            surface.blit(text_surface, text_rect)
            
            # Real-time validation feedback
            if self.chute.isdigit():
                num = int(self.chute)
                if num > 100:
                    error_text = "Máximo: 100"
                    error_surface = fonte_pequena.render(error_text, True, VERMELHO_NEON)
                    error_rect = error_surface.get_rect(center=(field_rect.centerx, field_rect.bottom + 20))
                    surface.blit(error_surface, error_rect)
        
        # Enhanced blinking cursor
        self.input_blink += 1
        if self.input_blink % 60 < 30:
            cursor_x = field_rect.centerx + (len(self.chute) * 12) if self.chute else field_rect.centerx
            cursor_color = VERDE_NEON if is_valid else VERMELHO_NEON
            pygame.draw.line(surface, cursor_color, (cursor_x, field_rect.centery - 15), 
                           (cursor_x, field_rect.centery + 15), 3)
        
        # Input hints
        hint_y = field_rect.bottom + 40
        hints = [
            "💡 ENTER: Confirmar | BACKSPACE: Apagar | DELETE: Limpar tudo",
            "🎯 Dica: A resposta está entre 0 e 100"
        ]
        
        for i, hint in enumerate(hints):
            hint_surface = fonte_pequena.render(hint, True, CINZA_MEDIO)
            hint_rect = hint_surface.get_rect(center=(LARGURA//2, hint_y + i*20))
            surface.blit(hint_surface, hint_rect)
    
    def draw_holographic_display(self, surface, texto, x, y, cor):
        """Desenha display holográfico"""
        # Efeito de holograma simplificado
        for offset in range(3):
            alpha = 100 - offset * 30
            offset_surface = fonte_texto.render(texto, True, cor)
            surface.blit(offset_surface, (x + offset, y + offset))
        
        # Linhas de varredura simplificadas
        for i in range(0, fonte_texto.get_height(), 3):
            pygame.draw.line(surface, cor, (x, y + i), (x + 400, y + i), 1)
    
    def update_effects(self):
        """Atualiza todos os efeitos visuais"""
        self.pulse_effect = math.sin(time.time() * 4) * 0.1 + 1
        self.glitch_effect = random.random() < 0.05
        
        # Adicionar partículas aleatórias
        if random.random() < 0.1:
            self.particles.add_particle(
                random.randint(0, LARGURA),
                random.randint(0, ALTURA),
                random.choice([AZUL_CYBER, VERDE_NEON, ROXO_ESPACIAL])
            )
    
    def processar_introducao(self):
        tempo_atual = time.time()
        
        if self.mensagem_atual < len(self.mensagens_intro):
            if tempo_atual >= self.tempo_proxima_mensagem:
                self.mensagem_atual += 1
                if self.mensagem_atual < len(self.mensagens_intro):
                    self.tempo_proxima_mensagem = tempo_atual + self.tempo_mensagens[self.mensagem_atual]
                else:
                    self.estado = "timer"
                    self.tempo_timer = tempo_atual + 1
    
    def processar_timer(self):
        tempo_atual = time.time()
        
        if tempo_atual >= self.tempo_timer:
            self.contador_timer -= 1
            if self.contador_timer > 0:
                self.tempo_timer = tempo_atual + 1
            else:
                self.estado = "jogo"
    
    def processar_chute(self):
        # This method should only be called when there's a valid input to process
        pass
    
    def processar_input_chute(self):
        """Process the guess input"""
        try:
            chute_int = int(self.chute)
            self.tentativas += 1
            self.historico_chutes.append(chute_int)
            
            # Adicionar partículas no chute
            for _ in range(20):
                self.particles.add_particle(
                    LARGURA//2, 300,
                    AZUL_CYBER if chute_int != 42 else AMARELO_OURO
                )
            
            if chute_int == 42 and chute_int == self.numero_secreto:
                self.estado = "vitoria"
            elif chute_int == 42 and chute_int != self.numero_secreto:
                self.tentativa_bonus += 1
                self.tentativas -= 1
                self.estado = "bonus_42"
            elif chute_int == self.numero_secreto:
                self.estado = "vitoria"
            else:
                self.estado = "dica"
            
            self.chute_atual = chute_int
            self.chute = ""
            
        except ValueError:
            pass
    
    def desenhar_introducao(self):
        self.draw_gradient_background(tela)
        self.particles.update_and_draw(tela)
        
        # Título com efeito especial
        self.draw_text_with_effect(tela, "🌌 GUIA DO MOCHILEIRO DAS GALÁXIAS 🌌", 
                                 LARGURA//2, 80, AMARELO_OURO, "rainbow", fonte_titulo_grande)
        
        # Mostrar mensagens com efeitos
        y = 180
        for i in range(min(self.mensagem_atual + 1, len(self.mensagens_intro))):
            mensagem = self.mensagens_intro[i]
            
            self.draw_text_with_effect(tela, mensagem["texto"], LARGURA//2, y, 
                                     mensagem["cor"], mensagem["efeito"])
            y += 50
    
    def desenhar_timer(self):
        self.draw_gradient_background(tela)
        self.particles.update_and_draw(tela)
        
        self.draw_text_with_effect(tela, "🌌 GUIA DO MOCHILEIRO DAS GALÁXIAS 🌌", 
                                 LARGURA//2, 80, AMARELO_OURO, "pulse", fonte_titulo_grande)
        
        self.draw_text_with_effect(tela, "⏰ CONTAGEM REGRESSIVA ⏰", 
                                 LARGURA//2, 200, VERMELHO_NEON, "pulse", fonte_titulo)
        
        # Timer gigante com efeitos
        timer_texto = str(self.contador_timer) if self.contador_timer > 0 else "GO!"
        cor_timer = VERMELHO_NEON if self.contador_timer <= 2 else AMARELO_OURO
        efeito_timer = "glitch" if self.contador_timer <= 2 else "pulse"
        
        self.draw_text_with_effect(tela, timer_texto, LARGURA//2, 350, 
                                 cor_timer, efeito_timer, fonte_gigante)
        
        # Adicionar partículas no timer baixo
        if self.contador_timer <= 2:
            for _ in range(5):
                self.particles.add_particle(LARGURA//2, 350, VERMELHO_NEON)
    
    def draw_progress_indicator(self, surface):
        """Draw a visual progress indicator based on attempts"""
        max_attempts = 10  # Reasonable max for visual representation
        progress = min(self.tentativas / max_attempts, 1.0)
        
        # Progress bar background
        bar_rect = pygame.Rect(LARGURA//2 - 150, 180, 300, 20)
        pygame.draw.rect(surface, CINZA_ESCURO, bar_rect, border_radius=10)
        
        # Progress fill with color coding
        if progress < 0.5:
            fill_color = VERDE_NEON
        elif progress < 0.8:
            fill_color = AMARELO_OURO
        else:
            fill_color = VERMELHO_NEON
        
        fill_width = int(bar_rect.width * progress)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, fill_width, bar_rect.height)
            pygame.draw.rect(surface, fill_color, fill_rect, border_radius=10)
        
        # Progress bar border
        pygame.draw.rect(surface, BRANCO, bar_rect, 2, border_radius=10)
        
        # Progress text
        progress_text = f"Tentativas: {self.tentativas}"
        if self.tentativas > max_attempts:
            progress_text += " (Persistente!)" 
        
        text_surface = fonte_pequena.render(progress_text, True, BRANCO)
        text_rect = text_surface.get_rect(center=(LARGURA//2, bar_rect.bottom + 15))
        surface.blit(text_surface, text_rect)
    
    def draw_smart_hints(self, surface):
        """Draw contextual hints based on game state"""
        hints = []
        
        if self.tentativas == 0:
            hints.append("💭 Primeira tentativa! Que tal começar com 50?")
        elif len(self.historico_chutes) >= 2:
            last_two = self.historico_chutes[-2:]
            if abs(last_two[1] - last_two[0]) > 20:
                hints.append("🎯 Tente números mais próximos entre si")
            elif last_two[1] == last_two[0]:
                hints.append("🔄 Você repetiu o mesmo número!")
        
        if self.tentativas >= 5:
            hints.append("🤔 Use a estratégia de busca binária!")
        
        if 42 in self.historico_chutes:
            hints.append("✨ Você já descobriu o segredo do universo!")
        
        # Draw hints
        y_offset = 520
        for hint in hints:
            hint_surface = fonte_pequena.render(hint, True, AZUL_CYBER)
            hint_rect = hint_surface.get_rect(center=(LARGURA//2, y_offset))
            surface.blit(hint_surface, hint_rect)
            y_offset += 25
    
    def desenhar_jogo(self):
        self.draw_gradient_background(tela)
        self.particles.update_and_draw(tela)
        
        # Animated title
        self.draw_text_with_effect(tela, "⚡ GERADOR DE IMPROBABILIDADE INFINITA ⚡", 
                                 LARGURA//2, 50, AZUL_CYBER, "wave", fonte_titulo)
        
        # Enhanced HUD
        hud_rect = pygame.Rect(50, 100, LARGURA-100, 70)
        pygame.draw.rect(tela, CINZA_ESCURO, hud_rect, border_radius=15)
        pygame.draw.rect(tela, AZUL_CYBER, hud_rect, 2, border_radius=15)
        
        # Game information with better layout
        info_text = f"📊 TENTATIVAS: {self.tentativas}"
        if self.tentativa_bonus > 0:
            info_text += f" | 🎁 BÔNUS: {self.tentativa_bonus}"
        
        self.draw_holographic_display(tela, info_text, 80, 130, BRANCO)
        
        # Progress indicator
        self.draw_progress_indicator(tela)
        
        # Input field with enhanced title
        self.draw_text_with_effect(tela, "🎯 Digite seu número (0-100):", 
                                 LARGURA//2, 250, BRANCO, "normal", fonte_titulo)
        
        self.draw_input_field(tela)
        
        # Enhanced history display
        if self.historico_chutes:
            self.draw_text_with_effect(tela, "📈 HISTÓRICO DE CHUTES", 
                                     LARGURA//2, 450, AMARELO_OURO, "normal", fonte_titulo)
            
            # Show last 5 guesses with better visual feedback
            y = 480
            for i, chute in enumerate(self.historico_chutes[-5:]):
                x = LARGURA//2 - 100 + (i * 40)
                
                # Color coding based on proximity to secret number
                if chute == 42:
                    cor = AMARELO_OURO
                    efeito = "pulse"
                elif abs(chute - self.numero_secreto) <= 5:
                    cor = VERDE_NEON
                    efeito = "normal"
                elif abs(chute - self.numero_secreto) <= 15:
                    cor = AZUL_CYBER
                    efeito = "normal"
                else:
                    cor = CINZA_MEDIO
                    efeito = "normal"
                
                self.draw_text_with_effect(tela, str(chute), x, y, cor, efeito)
        
        # Smart contextual hints
        self.draw_smart_hints(tela)
    
    def desenhar_dica(self):
        self.draw_gradient_background(tela)
        self.particles.update_and_draw(tela)
        
        # Adicionar partículas de erro
        for _ in range(3):
            self.particles.add_particle(LARGURA//2, 200, VERMELHO_NEON)
        
        self.draw_text_with_effect(tela, "❌ VOCÊ ERROU! ❌", 
                                 LARGURA//2, 150, VERMELHO_NEON, "glitch", fonte_titulo_grande)
        
        if self.chute_atual > self.numero_secreto:
            dica = f"⬇️ A resposta é um número MENOR que {self.chute_atual}"
            cor_dica = AZUL_CYBER
        else:
            dica = f"⬆️ A resposta é um número MAIOR que {self.chute_atual}"
            cor_dica = LARANJA_NEON
        
        self.draw_text_with_effect(tela, dica, LARGURA//2, 250, cor_dica, "pulse", fonte_titulo)
        
        self.draw_text_with_effect(tela, "🚀 Pressione ESPAÇO para continuar", 
                                 LARGURA//2, 400, CINZA_MEDIO, "fade")
    
    def desenhar_bonus_42(self):
        self.draw_gradient_background(tela)
        self.particles.update_and_draw(tela)
        
        # Explosão de partículas douradas
        for _ in range(10):
            self.particles.add_particle(LARGURA//2, 150, AMARELO_OURO)
        
        self.draw_text_with_effect(tela, "🎉 BÔNUS DE MOCHILEIRO! 🎉", 
                                 LARGURA//2, 100, AMARELO_OURO, "rainbow", fonte_titulo_grande)
        
        mensagens_bonus = [
            "42 já foi a resposta um dia.",
            "Tente acertar a nova resposta do gerador",
            "de improbabilidade infinita.",
            "",
            "Porém, você ganhou um bônus de mochileiro das galáxias.",
            "Essa tentativa não será computada.",
            "",
            "Tente novamente..."
        ]
        
        y = 180
        for linha in mensagens_bonus:
            if linha.strip():
                cor = VERDE_NEON if "bônus" in linha.lower() else AZUL_CYBER
                efeito = "pulse" if "bônus" in linha.lower() else "normal"
                self.draw_text_with_effect(tela, linha, LARGURA//2, y, cor, efeito)
            y += 35
        
        # Dica
        if self.chute_atual > self.numero_secreto:
            dica = f"⬇️ A resposta é um número MENOR que {self.chute_atual}"
        else:
            dica = f"⬆️ A resposta é um número MAIOR que {self.chute_atual}"
        
        self.draw_text_with_effect(tela, dica, LARGURA//2, 450, BRANCO, "pulse")
        
        # Instrução para continuar
        self.draw_text_with_effect(tela, "🚀 Pressione ESPAÇO para continuar", 
                                 LARGURA//2, 520, CINZA_MEDIO, "fade")
    
    def get_achievement_text(self):
        """Get achievement text based on performance"""
        achievements = []
        
        if self.numero_secreto == 42:
            achievements.append("🌟 MESTRE DO UNIVERSO")
        
        if self.tentativas == 1:
            achievements.append("🎯 TIRO CERTEIRO")
        elif self.tentativas <= 3:
            achievements.append("⚡ VELOCIDADE DA LUZ")
        elif self.tentativas <= 5:
            achievements.append("🧠 ESTRATEGISTA")
        elif self.tentativas <= 10:
            achievements.append("🎲 PERSISTENTE")
        else:
            achievements.append("🔄 DETERMINADO")
        
        if self.tentativa_bonus > 0:
            achievements.append("🎁 COLECIONADOR DE BÔNUS")
        
        if 42 in self.historico_chutes:
            achievements.append("🔍 EXPLORADOR CÓSMICO")
        
        return achievements
    
    def draw_fireworks_effect(self, surface):
        """Draw animated fireworks effect"""
        import math
        
        # Create multiple firework bursts
        for i in range(3):
            center_x = LARGURA//4 + (i * LARGURA//4)
            center_y = 150 + (i % 2) * 100
            
            # Animated burst effect
            time_factor = (pygame.time.get_ticks() / 1000.0) % 2
            radius = int(30 + time_factor * 20)
            
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                x = center_x + math.cos(rad) * radius
                y = center_y + math.sin(rad) * radius
                
                # Fade effect
                alpha = max(0, 255 - int(time_factor * 127))
                color = (*AMARELO_OURO[:3], alpha) if len(AMARELO_OURO) == 3 else AMARELO_OURO
                
                pygame.draw.circle(surface, AMARELO_OURO, (int(x), int(y)), 3)
    
    def desenhar_vitoria(self):
        self.draw_gradient_background(tela)
        self.particles.update_and_draw(tela)
        
        # Enhanced victory particle effects
        for _ in range(5):
            self.particles.add_particle(random.randint(0, LARGURA), random.randint(0, ALTURA//2), AMARELO_OURO)
            self.particles.add_particle(random.randint(0, LARGURA), random.randint(0, ALTURA//2), VERDE_NEON)
        
        # Fireworks effect
        self.draw_fireworks_effect(tela)
        
        # Epic victory title with enhanced animation
        self.draw_text_with_effect(tela, "🎉 PARABÉNS, MOCHILEIRO! 🎉", 
                                 LARGURA//2, 80, AMARELO_OURO, "pulse", fonte_titulo)
        
        # Special message with better formatting
        if self.numero_secreto == 42:
            self.draw_text_with_effect(tela, "✨ Você descobriu a Resposta para ✨", 
                                     LARGURA//2, 140, VERDE_NEON, "wave", fonte_titulo)
            self.draw_text_with_effect(tela, "🌌 a Vida, o Universo e Tudo Mais! 🌌", 
                                     LARGURA//2, 170, VERDE_NEON, "wave", fonte_titulo)
        else:
            self.draw_text_with_effect(tela, f"🎯 O número era {self.numero_secreto}! 🎯", 
                                     LARGURA//2, 150, VERDE_NEON, "normal", fonte_titulo)
        
        # Performance statistics with better layout
        stats_y = 220
        self.draw_text_with_effect(tela, f"📊 Tentativas: {self.tentativas}", 
                                 LARGURA//2, stats_y, BRANCO, "normal", fonte_titulo)
        
        if self.tentativa_bonus > 0:
            self.draw_text_with_effect(tela, f"🎁 Bônus de Mochileiro: {self.tentativa_bonus}", 
                                     LARGURA//2, stats_y + 30, AZUL_CYBER, "pulse", fonte_titulo)
            stats_y += 30
        
        # Achievement system
        achievements = self.get_achievement_text()
        if achievements:
            self.draw_text_with_effect(tela, "🏆 CONQUISTAS DESBLOQUEADAS 🏆", 
                                     LARGURA//2, stats_y + 60, AMARELO_OURO, "normal", fonte_titulo)
            
            for i, achievement in enumerate(achievements[:3]):  # Show max 3 achievements
                self.draw_text_with_effect(tela, achievement, 
                                         LARGURA//2, stats_y + 90 + (i * 25), 
                                         VERDE_NEON, "fade", fonte_pequena)
        
        # Enhanced buttons with better positioning
        button_y = ALTURA - 120
        self.restart_button.rect.centery = button_y
        self.quit_button.rect.centery = button_y
        
        # Update and draw buttons
        mouse_pos = pygame.mouse.get_pos()
        self.restart_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
        
        self.restart_button.draw(tela)
        self.quit_button.draw(tela)
        
        # Fun fact display
        fun_fact = "💡 Curiosidade: 42 é a resposta no livro 'O Guia do Mochileiro das Galáxias'"
        self.draw_text_with_effect(tela, fun_fact, LARGURA//2, ALTURA - 50, AZUL_CYBER, "fade", fonte_pequena)
    
    def desenhar(self):
        """Main drawing method that calls the appropriate drawing function"""
        if self.estado == "introducao":
            self.desenhar_introducao()
        elif self.estado == "timer":
            self.desenhar_timer()
        elif self.estado == "jogo":
            self.desenhar_jogo()
        elif self.estado == "dica":
            self.desenhar_dica()
        elif self.estado == "bonus_42":
            self.desenhar_bonus_42()
        elif self.estado == "vitoria":
            self.desenhar_vitoria()
    
    def reiniciar_jogo(self):
        self.__init__()    
    def handle_events(self):
        """Centralized event handling for better UX"""
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            elif evento.type == pygame.KEYDOWN:
                # Global shortcuts
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_F11:
                    # Toggle fullscreen
                    pygame.display.toggle_fullscreen()
                
                # State-specific input handling
                if self.estado == "introducao":
                    if evento.key == pygame.K_SPACE:
                        # Skip intro
                        self.estado = "timer"
                        self.tempo_timer = time.time() + 1
                
                elif self.estado == "timer":
                    if evento.key == pygame.K_SPACE:
                        # Skip countdown
                        self.estado = "jogo"
                
                elif self.estado == "jogo":
                    if evento.key == pygame.K_RETURN and self.chute:
                        self.processar_input_chute()
                    elif evento.key == pygame.K_BACKSPACE:
                        self.chute = self.chute[:-1]
                    elif evento.unicode.isdigit() and len(self.chute) < 3:
                        self.chute += evento.unicode
                    elif evento.key == pygame.K_DELETE:
                        self.chute = ""  # Clear entire input
                
                elif self.estado in ["dica", "bonus_42"]:
                    if evento.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.estado = "jogo"
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Left click
                    if self.estado == "vitoria":
                        if self.restart_button.is_clicked(mouse_pos, True):
                            self.reiniciar_jogo()
                        elif self.quit_button.is_clicked(mouse_pos, True):
                            return False
                    
                    # Allow clicking to skip intro/timer
                    elif self.estado == "introducao":
                        self.estado = "timer"
                        self.tempo_timer = time.time() + 1
                    elif self.estado == "timer":
                        self.estado = "jogo"
                    elif self.estado in ["dica", "bonus_42"]:
                        self.estado = "jogo"
        
        return True
    
    def update_game_state(self):
        """Update game logic based on current state"""
        if self.estado == "introducao":
            self.processar_introducao()
        elif self.estado == "timer":
            self.processar_timer()
    
    def executar(self):
        """Main game loop with improved UX"""
        clock = pygame.time.Clock()
        rodando = True
        
        # Show initial instructions
        print("🌌 Guia do Mochileiro das Galáxias - Controles:")
        print("   ESPAÇO: Pular introdução/timer")
        print("   ESC: Sair do jogo")
        print("   F11: Tela cheia")
        print("   DELETE: Limpar entrada")
        
        while rodando:
            # Handle events
            rodando = self.handle_events()
            if not rodando:
                break
            
            # Update game state
            self.update_game_state()
            
            # Update visual effects
            self.update_effects()
            
            # Draw everything
            self.desenhar()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()  
        

# Executar o jogo
if __name__ == "__main__":
    jogo = JogoAdivinhacao()
    jogo.executar()