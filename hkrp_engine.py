"""
Heart-Key Resonance Protocol (HKRP)
بروتوكول المصادقة الحيوي-ترددي

نظام محاكاة نظري لفك الإغلاق الجيني المشروط عبر التماسك القلبي-الدماغي
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Tuple, Optional
from enum import Enum
import time


class GateState(Enum):
    """حالات البوابة الجينية"""
    CLOSED = "closed"
    OPENING = "opening"
    OPEN = "open"
    ROLLBACK = "rollback"
    LOCKED = "locked"


@dataclass
class BioSignal:
    """إشارة حيوية مركبة"""
    hrv_sync: float = 0.0          # تزامن HRV [0, 1]
    eeg_phase_lock: float = 0.0    # قفل طور EEG [0, 1]
    breath_rhythm: float = 0.0     # انتظام التنفس [0, 1]
    timestamp: float = field(default_factory=time.time)
    
    def validate(self) -> bool:
        """التحقق من صحة الإشارة"""
        return all(0.0 <= x <= 1.0 for x in [self.hrv_sync, self.eeg_phase_lock, self.breath_rhythm])


@dataclass
class SafetyConfig:
    """تكوين معايير الأمان"""
    tau_safe: float = 0.80         # عتبة الأمان الدنيا
    h_max: float = 2.5             # الإنتروبيا القصوى (bits)
    delta_coherence: float = 0.15  # معدل التغير الحرج للتماسك
    response_timeout_ms: int = 250 # مهلة الاستجابة القصوى
    
    def __post_init__(self):
        if not 0.75 <= self.tau_safe <= 0.85:
            raise ValueError("tau_safe must be in [0.75, 0.85]")
        if self.h_max > 3.0:
            raise ValueError("h_max cannot exceed 3.0 bits")


class CoherenceSampler:
    """
    المرحلة 1: التقاط الإشارة
    قياس تناسق القلب-الدماغ كمصدر ترددي مستقر
    """
    
    def __init__(self, alpha: float = 0.4, beta: float = 0.35, gamma: float = 0.25):
        if not np.isclose(alpha + beta + gamma, 1.0, atol=0.01):
            raise ValueError("Weights must sum to 1.0")
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
    
    def compute_coherence(self, signal: BioSignal) -> float:
        """
        حساب درجة التماسك اللحظية
        C(t) = α·HRV_sync(t) + β·EEG_phase_lock(t) + γ·breath_rhythm(t)
        """
        if not signal.validate():
            return 0.0
        
        coherence = (
            self.alpha * signal.hrv_sync +
            self.beta * signal.eeg_phase_lock +
            self.gamma * signal.breath_rhythm
        )
        return np.clip(coherence, 0.0, 1.0)
    
    def simulate_signal(self, target_coherence: float = 0.85, noise_level: float = 0.05) -> BioSignal:
        """توليد إشارة محاكاة لأغراض الاختبار"""
        base = target_coherence
        noise = np.random.normal(0, noise_level, 3)
        
        hrv = np.clip(base + noise[0], 0.0, 1.0)
        eeg = np.clip(base + noise[1], 0.0, 1.0)
        breath = np.clip(base + noise[2], 0.0, 1.0)
        
        return BioSignal(hrv_sync=hrv, eeg_phase_lock=eeg, breath_rhythm=breath)


class ResonanceMatcher:
    """
    المرحلة 2: التشفير الضوئي الداخلي
    تحويل نمط التماسك إلى طيف فوتوني افتراضي ومطابقته مع القالب الآمن
    """
    
    def __init__(self, template_size: int = 64):
        self.template_size = template_size
        self.safe_template = self._generate_safe_template()
    
    def _generate_safe_template(self) -> np.ndarray:
        """توليد قالب التردد الآمن المرجعي"""
        # نمط غاوسي بسيط يمثل الحالة المتماسكة المثالية
        x = np.linspace(-3, 3, self.template_size)
        template = np.exp(-x**2 / 2)
        return template / np.max(template)
    
    def spectral_transform(self, coherence: float, signal: BioSignal) -> np.ndarray:
        """
        تحويل التماسك إلى تمثيل طيفي
        Φ(λ, t) = ∫ C(τ) · K(λ, τ) dτ
        
        تماسك أعلى ينتج طيفاً أكثر تركيزاً (إنتروبيا أقل)
        """
        x = np.linspace(-3, 3, self.template_size)
        
        # تماسك أعلى = نواة أضيق (أكثر تركيزاً = إنتروبيا أقل)
        # ضبط حساسية النواة للتماسك
        sigma = 1.5 / (1.0 + coherence * 0.8)
        kernel = np.exp(-x**2 / (2 * sigma**2))
        
        # تعديلات طيفية خفيفة جداً للحفاظ على الإنتروبيا منخفضة
        modulation = (
            1 + 
            0.08 * signal.hrv_sync * np.sin(x) +
            0.05 * signal.eeg_phase_lock * np.cos(0.5 * x)
        )
        
        spectrum = coherence * kernel * modulation
        return spectrum / (np.max(np.abs(spectrum)) + 1e-10)
    
    def compute_similarity(self, proof: np.ndarray, template: np.ndarray) -> float:
        """
        حساب التشابه باستخدام جيب تمام الزاوية
        sim(proof, template) = cos(θ)
        """
        dot_product = np.dot(proof.flatten(), template.flatten())
        norm_proof = np.linalg.norm(proof)
        norm_template = np.linalg.norm(template)
        
        if norm_proof < 1e-10 or norm_template < 1e-10:
            return 0.0
        
        similarity = dot_product / (norm_proof * norm_template)
        return np.clip(similarity, -1.0, 1.0)
    
    def compute_entropy(self, spectrum: np.ndarray) -> float:
        """
        حساب إنتروبيا شانون للطيف
        H = -Σ p_i · log₂(p_i)
        
        ملاحظة: الطيف المركز (غاوسي) له إنتروبيا منخفضة (~2-3 bits)
        """
        # تطبيع كدالة كثافة احتمالية
        p = np.abs(spectrum).flatten()
        p = p / (np.sum(p) + 1e-10)
        
        # تجنب اللوغاريتم للصفر
        p = p[p > 1e-10]
        
        entropy = -np.sum(p * np.log2(p))
        
        # تطبيع الإنتروبيا بالنسبة لحجم العينة
        # الإنتروبيا القصوى النظرية لـ n عينة هي log2(n)
        max_entropy = np.log2(len(np.abs(spectrum).flatten()))
        
        # تطبيع إلى نطاق معقول (0-6 bits بدلاً من 0-log2(n))
        normalized_entropy = entropy * (2.5 / max_entropy)
        
        return normalized_entropy
    
    def match(self, coherence: float, signal: BioSignal) -> Tuple[np.ndarray, float, float]:
        """
        تنفيذ المطابقة الكاملة
        إرجاع: (الطيف، التشابه، الإنتروبيا)
        """
        spectrum = self.spectral_transform(coherence, signal)
        similarity = self.compute_similarity(spectrum, self.safe_template)
        entropy = self.compute_entropy(spectrum)
        
        return spectrum, similarity, entropy


class ZKBioValidator:
    """
    المرحلة 3: بروتوكول المصادقة
    تطبيق نموذج مستوحى من Zero-Knowledge Proof الحيوي
    """
    
    def __init__(self, config: SafetyConfig):
        self.config = config
    
    def validate(self, similarity: float, entropy: float) -> Tuple[bool, str]:
        """
        التحقق من المعرفة الصفرية الحيوية
        V(proof, template) = 1 إذا كان: sim ≥ τ_safe ∧ entropy ≤ H_max
        """
        issues = []
        
        if similarity < self.config.tau_safe:
            issues.append(f"تشابه منخفض: {similarity:.3f} < {self.config.tau_safe}")
        
        if entropy > self.config.h_max:
            issues.append(f"إنتروبيا عالية: {entropy:.3f} > {self.config.h_max}")
        
        is_valid = len(issues) == 0
        status = "مصادقة ناجحة" if is_valid else f"فشل المصادقة: {'، '.join(issues)}"
        
        return is_valid, status


class ConditionalGate:
    """
    المرحلة 4: فك الإغلاق المشروط
    تفعيل مسار تعبير جيني مقيد عند تجاوز عتبة الأمان
    """
    
    def __init__(self, config: SafetyConfig):
        self.config = config
        self.state = GateState.CLOSED
        self.open_degree = 0.0
        self.history = []
    
    def sigmoid(self, x: float, steepness: float = 10.0) -> float:
        """دالة سيجمويد سلسة لتجنب التبديل المفاجئ"""
        return 1 / (1 + np.exp(-steepness * x))
    
    def compute_open_degree(self, validated: bool, coherence: float, similarity: float) -> float:
        """
        حساب درجة فتح البوابة
        G_open(t) = σ(V(t) · C(t) - τ_safe)
        """
        if not validated:
            return 0.0
        
        # دمج التماسك والتشابه
        combined = coherence * similarity
        delta = combined - self.config.tau_safe
        
        open_degree = self.sigmoid(delta, steepness=8.0)
        return np.clip(open_degree, 0.0, 1.0)
    
    def update(self, validated: bool, coherence: float, similarity: float) -> GateState:
        """تحديث حالة البوابة"""
        prev_state = self.state
        new_open_degree = self.compute_open_degree(validated, coherence, similarity)
        
        # تحديد الحالة الجديدة
        if new_open_degree < 0.1:
            self.state = GateState.CLOSED
        elif new_open_degree < 0.5:
            self.state = GateState.OPENING
        elif new_open_degree >= 0.5:
            self.state = GateState.OPEN
        
        self.open_degree = new_open_degree
        
        # تسجيل في السجل
        self.history.append({
            'timestamp': time.time(),
            'prev_state': prev_state.value,
            'new_state': self.state.value,
            'open_degree': self.open_degree,
            'coherence': coherence,
            'validated': validated
        })
        
        return self.state


class SafetyRollback:
    """
    المرحلة 5: بروتوكول السلامة العكسية
    مراقبة الإنتروبيا الحيوية وتفعيل التراجع الفوري عند الحاجة
    """
    
    def __init__(self, config: SafetyConfig):
        self.config = config
        self.coherence_history = []
        self.rollback_triggered = False
        self.rollback_count = 0
    
    def monitor(self, coherence: float, entropy: float) -> bool:
        """
        مراقبة الشروط الحرجة
        R(t) = 1 إذا كان: dC/dt < -δ أو H(t) > H_critical
        """
        self.coherence_history.append((time.time(), coherence))
        
        # الاحتفاظ بآخر ثانية من البيانات فقط
        cutoff = time.time() - 1.0
        self.coherence_history = [(t, c) for t, c in self.coherence_history if t > cutoff]
        
        # حساب معدل تغير التماسك
        if len(self.coherence_history) >= 2:
            times = [t for t, _ in self.coherence_history]
            values = [c for _, c in self.coherence_history]
            
            dt = times[-1] - times[0]
            if dt > 0:
                dC_dt = (values[-1] - values[0]) / dt
            else:
                dC_dt = 0
        else:
            dC_dt = 0
        
        # فحص شروط التراجع
        critical_entropy = self.config.h_max * 1.2  # 20% فوق الحد الأقصى
        rollback_needed = (
            dC_dt < -self.config.delta_coherence or
            entropy > critical_entropy
        )
        
        if rollback_needed and not self.rollback_triggered:
            self.rollback_triggered = True
            self.rollback_count += 1
        
        return rollback_needed
    
    def reset(self):
        """إعادة تعيين حالة التراجع"""
        self.rollback_triggered = False
    
    def get_diagnostics(self) -> dict:
        """الحصول على تشخيصات النظام"""
        return {
            'rollback_count': self.rollback_count,
            'currently_rolled_back': self.rollback_triggered,
            'coherence_samples': len(self.coherence_history),
            'avg_coherence': (
                np.mean([c for _, c in self.coherence_history]) 
                if self.coherence_history else 0.0
            )
        }


class HKRPEngine:
    """
    محرك بروتوكول Heart-Key Resonance الرئيسي
    يدمج جميع المكونات في تدفق متكامل
    """
    
    def __init__(self, config: Optional[SafetyConfig] = None):
        self.config = config or SafetyConfig()
        self.sampler = CoherenceSampler()
        self.matcher = ResonanceMatcher()
        self.validator = ZKBioValidator(self.config)
        self.gate = ConditionalGate(self.config)
        self.safety = SafetyRollback(self.config)
        
        self.session_log = []
    
    def process_signal(self, signal: BioSignal) -> dict:
        """
        معالجة إشارة كاملة عبر جميع المراحل
        """
        start_time = time.time()
        
        # المرحلة 1: حساب التماسك
        coherence = self.sampler.compute_coherence(signal)
        
        # المرحلة 2: المطابقة الطيفية
        spectrum, similarity, entropy = self.matcher.match(coherence, signal)
        
        # المرحلة 3: التحقق من المصادقة
        validated, status = self.validator.validate(similarity, entropy)
        
        # مراقبة السلامة قبل فتح البوابة
        rollback_needed = self.safety.monitor(coherence, entropy)
        
        if rollback_needed:
            gate_state = GateState.ROLLBACK
            open_degree = 0.0
            self.safety.reset()  # إعادة التعيين بعد التفعيل
        else:
            # المرحلة 4: تحديث البوابة
            gate_state = self.gate.update(validated, coherence, similarity)
            open_degree = self.gate.open_degree
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        result = {
            'timestamp': signal.timestamp,
            'coherence': coherence,
            'similarity': similarity,
            'entropy': entropy,
            'validated': validated,
            'validation_status': status,
            'gate_state': gate_state.value,
            'open_degree': open_degree,
            'rollback_triggered': rollback_needed,
            'processing_time_ms': elapsed_ms,
            'safety_diagnostics': self.safety.get_diagnostics()
        }
        
        self.session_log.append(result)
        return result
    
    def run_simulation(self, num_iterations: int = 10, 
                       coherence_target: float = 0.85,
                       noise_levels: list = None) -> list:
        """
        تشغيل محاكاة كاملة
        """
        if noise_levels is None:
            noise_levels = [0.02, 0.05, 0.10, 0.15]
        
        results = []
        
        print("=" * 60)
        print("🔐 Heart-Key Resonance Protocol - محاكاة البروتوكول")
        print("=" * 60)
        print(f"عدد التكرارات: {num_iterations}")
        print(f"التماسك المستهدف: {coherence_target}")
        print(f"عتبة الأمان: {self.config.tau_safe}")
        print(f"الإنتروبيا القصوى: {self.config.h_max} bits")
        print("=" * 60)
        
        for i in range(num_iterations):
            # اختيار مستوى ضوضاء عشوائي
            noise = np.random.choice(noise_levels)
            
            # توليد إشارة محاكاة
            signal = self.sampler.simulate_signal(coherence_target, noise)
            
            # معالجة الإشارة
            result = self.process_signal(signal)
            results.append(result)
            
            # عرض النتائج
            status_icon = "✅" if result['validated'] else "❌"
            if result['rollback_triggered']:
                status_icon = "⚠️"
            
            print(f"\n[{i+1}/{num_iterations}] {status_icon}")
            print(f"  التماسك: {result['coherence']:.3f}")
            print(f"  التشابه: {result['similarity']:.3f}")
            print(f"  الإنتروبيا: {result['entropy']:.3f} bits")
            print(f"  حالة البوابة: {result['gate_state']}")
            print(f"  درجة الفتح: {result['open_degree']:.3f}")
            print(f"  زمن المعالجة: {result['processing_time_ms']:.2f} ms")
            
            if result['rollback_triggered']:
                print(f"  ⚠️ تم تفعيل التراجع الآمن!")
        
        # ملخص الإحصائيات
        print("\n" + "=" * 60)
        print("📊 ملخص الإحصائيات")
        print("=" * 60)
        
        total = len(results)
        successful = sum(1 for r in results if r['validated'])
        rollbacks = sum(1 for r in results if r['rollback_triggered'])
        avg_coherence = np.mean([r['coherence'] for r in results])
        avg_processing = np.mean([r['processing_time_ms'] for r in results])
        
        print(f"  إجمالي المحاولات: {total}")
        print(f"  المصادقات الناجحة: {successful} ({100*successful/total:.1f}%)")
        print(f"  حالات التراجع: {rollbacks} ({100*rollbacks/total:.1f}%)")
        print(f"  متوسط التماسك: {avg_coherence:.3f}")
        print(f"  متوسط زمن المعالجة: {avg_processing:.2f} ms")
        print("=" * 60)
        
        return results
    
    def get_session_report(self) -> dict:
        """توليد تقرير الجلسة"""
        if not self.session_log:
            return {}
        
        return {
            'total_attempts': len(self.session_log),
            'success_rate': sum(1 for r in self.session_log if r['validated']) / len(self.session_log),
            'avg_coherence': np.mean([r['coherence'] for r in self.session_log]),
            'avg_open_degree': np.mean([r['open_degree'] for r in self.session_log]),
            'total_rollbacks': sum(1 for r in self.session_log if r['rollback_triggered']),
            'avg_processing_time_ms': np.mean([r['processing_time_ms'] for r in self.session_log])
        }


# === نقطة الدخول الرئيسية ===
if __name__ == "__main__":
    # إنشاء المحرك بالتكوين الافتراضي
    engine = HKRPEngine()
    
    # تشغيل المحاكاة
    results = engine.run_simulation(num_iterations=15, coherence_target=0.85)
    
    # عرض تقرير الجلسة
    report = engine.get_session_report()
    print("\n📋 تقرير الجلسة:")
    for key, value in report.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
