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
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Animação suave
        target_scale = 1.1 if self.is_hovered else 1.0
        self.animation_scale += (target_scale - self.animation_scale) * 0.1
        
        # Efeito de brilho
        target_glow = 20 if self.is_hovered else 0
        self.glow_intensity += (target_glow - self.glow_intensity) * 0.1
    
    def draw(self, surface):
        # Calcular retângulo animado
        center = self.rect.center
        new_width = int(self.rect.width * self.animation_scale)
        new_height = int(self.rect.height * self.animation_scale)
        animated_rect = pygame.Rect(0, 0, new_width, new_height)
        animated_rect.center = center
        
        # Desenhar brilho (sem alpha blending para evitar erros)
        if self.glow_intensity > 0:
            glow_rect = animated_rect.inflate(int(self.glow_intensity), int(self.glow_intensity))
            pygame.draw.rect(surface, self.hover_color, glow_rect, border_radius=15)
        
        # Desenhar botão
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, animated_rect, border_radius=15)
        pygame.draw.rect(surface, BRANCO, animated_rect, 2, border_radius=15)
        
        # Desenhar texto
        text_surface = fonte_texto.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=animated_rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        return self.rect.collidepoint(mouse_pos) and mouse_clicked

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
        """Desenha campo de entrada futurista"""
        # Campo principal
        field_rect = pygame.Rect(LARGURA//2 - 200, 300, 400, 60)
        
        # Brilho animado (simplificado)
        glow_intensity = int(20 + 10 * math.sin(time.time() * 3))
        for i in range(3):  # Reduced iterations to prevent performance issues
            glow_rect = field_rect.inflate(i*4, i*4)
            pygame.draw.rect(surface, AZUL_CYBER, glow_rect, border_radius=15, width=1)
        
        # Campo de entrada
        pygame.draw.rect(surface, CINZA_ESCURO, field_rect, border_radius=15)
        pygame.draw.rect(surface, AZUL_CYBER, field_rect, 3, border_radius=15)
        
        # Texto digitado
        if self.chute:
            text_surface = fonte_titulo.render(self.chute, True, BRANCO)
            text_rect = text_surface.get_rect(center=field_rect.center)
            surface.blit(text_surface, text_rect)
        
        # Cursor piscante
        self.input_blink += 1
        if self.input_blink % 60 < 30:  # Pisca a cada segundo
            cursor_x = field_rect.centerx + (len(self.chute) * 12)
            pygame.draw.line(surface, AZUL_CYBER, (cursor_x, field_rect.centery - 15), 
                           (cursor_x, field_rect.centery + 15), 2)
    
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
    
    def desenhar_jogo(self):
        self.draw_gradient_background(tela)
        self.particles.update_and_draw(tela)
        
        # Título animado
        self.draw_text_with_effect(tela, "⚡ GERADOR DE IMPROBABILIDADE INFINITA ⚡", 
                                 LARGURA//2, 50, AZUL_CYBER, "wave", fonte_titulo)
        
        # HUD futurista
        hud_rect = pygame.Rect(50, 100, LARGURA-100, 120)
        pygame.draw.rect(tela, CINZA_ESCURO, hud_rect, border_radius=15)
        pygame.draw.rect(tela, AZUL_CYBER, hud_rect, 2, border_radius=15)
        
        # Informações do jogo
        self.draw_holographic_display(tela, f"📊 TENTATIVAS: {self.tentativas}", 80, 130, BRANCO)
        
        if self.tentativa_bonus > 0:
            self.draw_text_with_effect(tela, f"🎁 BÔNUS DE MOCHILEIRO: {self.tentativa_bonus}", 
                                     LARGURA//2, 160, VERDE_NEON, "pulse")
        
        # Campo de entrada futurista
        self.draw_text_with_effect(tela, "🎯 Digite seu número (0-100):", 
                                 LARGURA//2, 250, BRANCO, "normal", fonte_titulo)
        
        self.draw_input_field(tela)
        
        # Instruções
        self.draw_text_with_effect(tela, "⚡ Pressione ENTER para confirmar ⚡", 
                                 LARGURA//2, 380, AZUL_CYBER, "fade", fonte_pequena)
        
        # Histórico de chutes com estilo
        if self.historico_chutes:
            self.draw_text_with_effect(tela, "📈 HISTÓRICO DE CHUTES", 
                                     LARGURA//2, 450, AMARELO_OURO, "normal", fonte_titulo)
            
            # Mostrar últimos 5 chutes em linha
            y = 490
            for i, chute in enumerate(self.historico_chutes[-5:]):
                x = LARGURA//2 - 100 + (i * 40)
                cor = AMARELO_OURO if chute == 42 else VERDE_NEON
                efeito = "pulse" if chute == 42 else "normal"
                self.draw_text_with_effect(tela, str(chute), x, y, cor, efeito)
    
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
    
    def desenhar_vitoria(self):
        self.draw_gradient_background(tela)
        self.particles.update_and_draw(tela)
        
        # Explosão de partículas de vitória
        for _ in range(30):
            cores_vitoria = [VERDE_NEON, AMARELO_OURO, AZUL_CYBER, ROXO_ESPACIAL]
            self.particles.add_particle(
                random.randint(0, LARGURA),
                random.randint(0, ALTURA),
                random.choice(cores_vitoria)
            )
        
        self.draw_text_with_effect(tela, "🎊 PARABÉNS! VOCÊ VENCEU! 🎊", 
                                 LARGURA//2, 100, AMARELO_OURO, "rainbow", fonte_titulo_grande)
        
        mensagens_vitoria = [
            f"Você descobriu a resposta em {self.tentativas} tentativas!",
            "A resposta para a vida, o universo e tudo mais é:",
            str(self.numero_secreto),
            "",
            "Mas será que essa é realmente a resposta?",
            "Ou será que o gerador de improbabilidade infinita",
            "está apenas brincando conosco?",
            "",
            "De qualquer forma, não entre em pânico!"
        ]
        
        y = 200
        for linha in mensagens_vitoria:
            if linha.strip():
                if linha == str(self.numero_secreto):
                    self.draw_text_with_effect(tela, linha, LARGURA//2, y, 
                                             VERDE_NEON, "glitch", fonte_gigante)
                    y += 80
                else:
                    cor = AZUL_CYBER if "resposta" in linha.lower() else BRANCO
                    efeito = "pulse" if "resposta" in linha.lower() else "normal"
                    self.draw_text_with_effect(tela, linha, LARGURA//2, y, 
                                             cor, efeito, fonte_titulo)
                    y += 40
            else:
                y += 20
        
        # Atualizar e desenhar botões
        mouse_pos = pygame.mouse.get_pos()
        self.restart_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
        
        self.restart_button.draw(tela)
        self.quit_button.draw(tela)
        
        self.draw_text_with_effect(tela, "🏆 RESPOSTA CORRETA! 🏆", 
                                 LARGURA//2, 100, VERDE_NEON, "rainbow", fonte_titulo_grande)
        
        self.draw_text_with_effect(tela, "🎊 FIM DE JOGO 🎊", 
                                 LARGURA//2, 150, AMARELO_OURO, "pulse", fonte_titulo)
        
        mensagem_final = f"Você acertou a resposta para a vida, o universo e tudo mais\ndo gerador de improbabilidade infinita em {self.tentativas} tentativas."
        
        y = 220
        for linha in mensagem_final.split('\n'):
            self.draw_text_with_effect(tela, linha.strip(), LARGURA//2, y, BRANCO, "normal")
            y += 35
        
        if self.tentativa_bonus > 0:
            bonus_msg = f"🎁 Você teve {min(self.tentativa_bonus, 1)} tentativa bônus de mochileiro das galáxias."
            self.draw_text_with_effect(tela, bonus_msg, LARGURA//2, 320, VERDE_NEON, "pulse")
        
        self.draw_text_with_effect(tela, f"🎯 Número secreto: {self.numero_secreto}", 
                                 LARGURA//2, 380, AMARELO_OURO, "wave")
        
        # Botões interativos
        mouse_pos = pygame.mouse.get_pos()
        self.restart_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
        
        self.restart_button.draw(tela)
        self.quit_button.draw(tela)
    
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
    
    def executar(self):
        clock = pygame.time.Clock()
        rodando = True
        
        while rodando:
            # Limitar FPS
            clock.tick(60)
            
            # Atualizar efeitos
            self.update_effects()
            
            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    sys.exit()
                
                elif evento.type == pygame.KEYDOWN:
                    if self.estado == "jogo":
                        if evento.key == pygame.K_RETURN and self.chute:
                            self.processar_input_chute()
                        elif evento.key == pygame.K_BACKSPACE:
                            self.chute = self.chute[:-1]
                        elif evento.unicode.isdigit() and len(self.chute) < 3:
                            self.chute += evento.unicode
                    
                    elif self.estado == "dica" or self.estado == "bonus_42":
                        if evento.key == pygame.K_SPACE:
                            self.estado = "jogo"
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:  # Botão esquerdo
                        mouse_pos = pygame.mouse.get_pos()
                        
                        if self.estado == "vitoria":
                            if self.restart_button.is_clicked(mouse_pos, True):
                                self.__init__()
                            elif self.quit_button.is_clicked(mouse_pos, True):
                                rodando = False
                                pygame.quit()
                                sys.exit()
            
            # Atualizar estado do jogo
            if self.estado == "introducao":
                self.processar_introducao()
                self.desenhar_introducao()
            elif self.estado == "timer":
                self.processar_timer()
                self.desenhar_timer()
            elif self.estado == "jogo":
                self.desenhar_jogo()
            elif self.estado == "dica":
                self.desenhar_dica()
            elif self.estado == "bonus_42":
                self.desenhar_bonus_42()
            elif self.estado == "vitoria":
                self.desenhar_vitoria()
            
            # Atualizar tela
            pygame.display.flip()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                
                elif evento.type == pygame.KEYDOWN:
                    if self.estado == "jogo":
                        if evento.key == pygame.K_RETURN:
                            if self.chute:
                                self.processar_input_chute()
                        elif evento.key == pygame.K_BACKSPACE:
                            self.chute = self.chute[:-1]
                        elif evento.unicode.isdigit():
                            if len(self.chute) < 3:
                                self.chute += evento.unicode
                    
                    elif self.estado in ["dica", "bonus_42"]:
                        if evento.key == pygame.K_SPACE:
                            self.estado = "jogo"
            
            # Handle mouse clicks for victory screen
            if self.estado == "vitoria":
                if self.restart_button.rect.collidepoint(mouse_pos):
                    self.reiniciar_jogo()
                elif self.quit_button.rect.collidepoint(mouse_pos):
                    rodando = False

            # Atualizar estado do jogo
            if self.estado == "introducao":
                self.processar_introducao()
            elif self.estado == "timer":
                self.processar_timer()
            elif self.estado == "jogo":
                self.processar_chute()

            # Desenhar
            self.desenhar()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()  
        

# Executar o jogo
if __name__ == "__main__":
    jogo = JogoAdivinhacao()
    jogo.executar()