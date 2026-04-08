--- Platinum-African-Project/genetic_encryption/warning_logger.py (原始)


+++ Platinum-African-Project/genetic_encryption/warning_logger.py (修改后)
"""
⚠️ Platinum African Project - Genetic Encryption Warning Log System
نظام سجلات تحذير التشوهات الوراثية

This module monitors and logs any anomalies or distortions detected
during genetic encryption operations. Critical for safety compliance.
"""

import numpy as np
import time
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class AnomalyType(Enum):
    """أنواع التشوهات الوراثية المحتملة"""
    INTEGRITY_LOSS = "integrity_loss"           # فقدان سلامة البيانات
    UNAUTHORIZED_ACCESS = "unauthorized_access"  # وصول غير مصرح به
    COHERENCE_DROP = "coherence_drop"           # انخفاض التماسك الحيوي
    ENCRYPTION_FAILURE = "encryption_failure"    # فشل التشفير
    MUTATION_DETECTED = "mutation_detected"      # طفرة مكتشفة
    EPIGENETIC_DRIFT = "epigenetic_drift"       # انحراف جيني
    QUANTUM_DECOHERENCE = "quantum_decoherence" # فك تماسك كمي


class SeverityLevel(Enum):
    """مستويات شدة التحذير"""
    LOW = "LOW"               # منخفض - ملاحظة روتينية
    MEDIUM = "MEDIUM"         # متوسط - يتطلب انتباهاً
    HIGH = "HIGH"             # عالي - يتطلب تدخلاً فورياً
    CRITICAL = "CRITICAL"     # حرج - إيقاف فوري للنظام


@dataclass
class WarningEntry:
    """سجل تحذير فردي"""
    id: str                              # معرف فريد
    timestamp: float                     # طابع زمني
    anomaly_type: str                    # نوع الشذوذ
    severity: str                        # مستوى الشدة
    affected_module: str                 # الوحدة المتأثرة
    description: str                     # وصف تفصيلي
    recovery_action: str                 # إجراء الاسترداد
    human_impact_assessment: str         # تقييم التأثير البشري
    data_snapshot: Dict                  # لقطة من البيانات
    resolved: bool = False               # هل تم الحل؟
    resolution_time: Optional[float] = None  # وقت الحل

    def to_dict(self) -> Dict:
        """تحويل السجل إلى قاموس"""
        return asdict(self)

    def to_json(self) -> str:
        """تحويل السجل إلى JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class GeneticIntrusionDetector:
    """
    نظام كشف التسلل الجيني

    يراقب تدفق البيانات الوراثية ويكشف عن أي تشوهات
    """

    def __init__(self, integrity_threshold: float = 0.99):
        """
        تهيئة كاشف التسلل

        Args:
            integrity_threshold: عتبة سلامة البيانات الدنيا
        """
        self.integrity_threshold = integrity_threshold
        self.alert_level = "GREEN"
        self.anomaly_history: List[WarningEntry] = []
        self.monitoring_active = True

        # إحصائيات المراقبة
        self.total_checks = 0
        self.anomalies_detected = 0
        self.critical_events = 0

    def calculate_integrity(self, data_stream: np.ndarray) -> float:
        """
        حساب سلامة تدفق البيانات

        Args:
            data_stream: تدفق البيانات الوراثية

        Returns:
            درجة السلامة (0-1)
        """
        if len(data_stream) == 0:
            return 0.0

        # حساب إحصائيات متعددة للسلامة
        mean_val = np.mean(data_stream)
        std_val = np.std(data_stream)

        # كشف القيم الشاذة
        z_scores = np.abs((data_stream - mean_val) / max(std_val, 1e-10))
        outlier_ratio = np.sum(z_scores > 3) / len(data_stream)

        # حساب التماسك الداخلي
        if len(data_stream) > 10:
            autocorr = np.correlate(data_stream - mean_val,
                                    data_stream - mean_val,
                                    mode='full')
            autocorr = autocorr[len(autocorr)//2:]
            coherence = autocorr[1] / max(autocorr[0], 1e-10) if len(autocorr) > 1 else 1.0
        else:
            coherence = 1.0

        # درجة السلامة المركبة
        integrity = (1 - outlier_ratio) * 0.6 + abs(coherence) * 0.4

        return min(max(integrity, 0.0), 1.0)

    def monitor(self, data_stream: np.ndarray,
                module_name: str = "unknown") -> Optional[WarningEntry]:
        """
        مراقبة تدفق البيانات وكشف التشوهات

        Args:
            data_stream: تدفق البيانات
            module_name: اسم الوحدة المراقبة

        Returns:
            WarningEntry إذا تم كشف شذوذ، None وإلا
        """
        if not self.monitoring_active:
            return None

        self.total_checks += 1

        integrity = self.calculate_integrity(data_stream)

        if integrity < self.integrity_threshold:
            self.anomalies_detected += 1

            # تحديد مستوى الشدة بناءً على حجم الانحراف
            deviation = self.integrity_threshold - integrity

            if deviation > 0.3:
                severity = SeverityLevel.CRITICAL
                self.critical_events += 1
            elif deviation > 0.2:
                severity = SeverityLevel.HIGH
            elif deviation > 0.1:
                severity = SeverityLevel.MEDIUM
            else:
                severity = SeverityLevel.LOW

            # إنشاء سجل التحذير
            warning = self._create_warning_entry(
                anomaly_type=AnomalyType.INTEGRITY_LOSS,
                severity=severity,
                affected_module=module_name,
                description=f"انخفاض سلامة البيانات إلى {integrity:.4f} (العتبة: {self.integrity_threshold})",
                recovery_action=self._determine_recovery_action(severity, integrity),
                human_impact_assessment=self._assess_human_impact(severity, integrity),
                data_snapshot={
                    'integrity_score': integrity,
                    'threshold': self.integrity_threshold,
                    'deviation': deviation,
                    'data_shape': data_stream.shape,
                    'data_mean': float(np.mean(data_stream)),
                    'data_std': float(np.std(data_stream))
                }
            )

            # تحديث مستوى التنبيه
            if severity == SeverityLevel.CRITICAL:
                self.alert_level = "RED"
                self.trigger_lockdown()
            elif severity == SeverityLevel.HIGH:
                self.alert_level = "ORANGE"
            elif severity == SeverityLevel.MEDIUM:
                self.alert_level = "YELLOW"

            return warning

        return None

    def _create_warning_entry(self, anomaly_type: AnomalyType,
                               severity: SeverityLevel,
                               affected_module: str,
                               description: str,
                               recovery_action: str,
                               human_impact_assessment: str,
                               data_snapshot: Dict) -> WarningEntry:
        """
        إنشاء سجل تحذير جديد

        Returns:
            WarningEntry جاهز
        """
        entry_id = f"WARN-{int(time.time())}-{np.random.randint(1000, 9999)}"

        warning = WarningEntry(
            id=entry_id,
            timestamp=time.time(),
            anomaly_type=anomaly_type.value,
            severity=severity.value,
            affected_module=affected_module,
            description=description,
            recovery_action=recovery_action,
            human_impact_assessment=human_impact_assessment,
            data_snapshot=data_snapshot,
            resolved=False
        )

        self.anomaly_history.append(warning)

        # طباعة تنبيه
        self._print_alert(warning)

        return warning

    def _determine_recovery_action(self, severity: SeverityLevel,
                                   integrity: float) -> str:
        """تحديد إجراء الاسترداد المناسب"""
        if severity == SeverityLevel.CRITICAL:
            return "🛑 إيقاف فوري للنظام | عزل القنوات | استعادة آخر نسخة سليمة | إشعار لجنة الأخلاقيات"
        elif severity == SeverityLevel.HIGH:
            return "⚠️ تفعيل بروتوكول التراجع | زيادة تردد المراقبة | تحضير للاسترداد"
        elif severity == SeverityLevel.MEDIUM:
            return "📊 تسجيل مفصل للشذوذ | مراجعة الخوارزمية | مراقبة مكثفة"
        else:
            return "📝 تسجيل روتيني | متابعة في المراجعة الدورية"

    def _assess_human_impact(self, severity: SeverityLevel,
                            integrity: float) -> str:
        """تقييم التأثير البشري المحتمل"""
        if severity == SeverityLevel.CRITICAL:
            if integrity < 0.5:
                return "CONFIRMED - خطر تشوه وراثي جسيم محتمل"
            else:
                return "POTENTIAL - خطر متوسط، يتطلب فحصاً إضافياً"
        elif severity == SeverityLevel.HIGH:
            return "POTENTIAL - تأثير طفيف محتمل، مراقبة ضرورية"
        elif severity == SeverityLevel.MEDIUM:
            return "LOW - تأثير ضئيل جداً متوقع"
        else:
            return "NONE - لا تأثير بشري متوقع"

    def _print_alert(self, warning: WarningEntry) -> None:
        """طباعة تنبيه مرئي"""
        emoji_map = {
            "LOW": "📝",
            "MEDIUM": "⚠️",
            "HIGH": "🚨",
            "CRITICAL": "🛑"
        }

        emoji = emoji_map.get(warning.severity, "❓")

        print(f"\n{emoji} [{warning.severity}] {warning.anomaly_type}")
        print(f"   📍 الوحدة: {warning.affected_module}")
        print(f"   📄 الوصف: {warning.description}")
        print(f"   🔧 الإجراء: {warning.recovery_action}")
        print(f"   👤 التأثير البشري: {warning.human_impact_assessment}")
        print(f"   ⏰ الوقت: {datetime.fromtimestamp(warning.timestamp).isoformat()}")

    def trigger_lockdown(self) -> None:
        """تفعيل حالة الإغلاق الطارئ"""
        print("\n" + "=" * 70)
        print("🛑 LOCKDOWN ACTIVATED - إغلاق طارئ مفعّل")
        print("=" * 70)
        print("   • جميع القنوات معزولة")
        print("   • بروتوكول التراجع مُفعّل")
        print("   • المشرفون تم إشعارهم")
        print("   • السجلات تم حفظها بأمان")
        print("=" * 70 + "\n")

        self.monitoring_active = False

    def get_statistics(self) -> Dict:
        """الحصول على إحصائيات النظام"""
        severity_counts = {level.value: 0 for level in SeverityLevel}
        for entry in self.anomaly_history:
            severity_counts[entry.severity] += 1

        return {
            'total_checks': self.total_checks,
            'anomalies_detected': self.anomalies_detected,
            'critical_events': self.critical_events,
            'alert_level': self.alert_level,
            'monitoring_active': self.monitoring_active,
            'severity_breakdown': severity_counts,
            'detection_rate': self.anomalies_detected / max(self.total_checks, 1)
        }


class WarningLogSystem:
    """
    نظام إدارة سجلات التحذير

    يوفر واجهة شاملة لتسجيل واستعلام وتحليل التحذيرات
    """

    def __init__(self, log_directory: str = "warning_logs"):
        """
        تهيئة نظام السجلات

        Args:
            log_directory: مجلد حفظ السجلات
        """
        self.log_directory = log_directory
        self.detector = GeneticIntrusionDetector()
        self.logs: List[WarningEntry] = []

        # إنشاء مجلد السجلات إذا لم يوجد
        os.makedirs(log_directory, exist_ok=True)

        print(f"📂 نظام سجلات التحذير مُهيأ في: {log_directory}")

    def log_anomaly(self, data_stream: np.ndarray,
                   module_name: str,
                   anomaly_override: Optional[AnomalyType] = None) -> Optional[WarningEntry]:
        """
        تسجيل شذوذ بعد تحليل البيانات

        Args:
            data_stream: تدفق البيانات
            module_name: اسم الوحدة
            anomaly_override: تجاوز نوع الشذوذ (اختياري)

        Returns:
            WarningEntry إذا تم تسجيل شذوذ
        """
        warning = self.detector.monitor(data_stream, module_name)

        if warning:
            self.logs.append(warning)

            # حفظ السجل فوراً
            self._save_log(warning)

        return warning

    def _save_log(self, warning: WarningEntry) -> str:
        """
        حفظ سجل في الملف

        Returns:
            مسار الملف المحفوظ
        """
        date_str = datetime.fromtimestamp(warning.timestamp).strftime("%Y-%m-%d")
        filename = f"{date_str}_{warning.severity}_{warning.id}.json"
        filepath = os.path.join(self.log_directory, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(warning.to_json())

        return filepath

    def resolve_warning(self, warning_id: str,
                       resolution_notes: str = "") -> bool:
        """
        حل تحذير مسجل

        Args:
            warning_id: معرف التحذير
            resolution_notes: ملاحظات الحل

        Returns:
            True إذا تم الحل بنجاح
        """
        for log in self.logs:
            if log.id == warning_id:
                log.resolved = True
                log.resolution_time = time.time()

                # تحديث الملف المحفوظ
                self._save_log(log)

                print(f"✅ تم حل التحذير {warning_id}")
                print(f"   📝 ملاحظات: {resolution_notes}")

                return True

        print(f"❌ التحذير {warning_id} غير موجود")
        return False

    def get_critical_logs(self) -> List[WarningEntry]:
        """الحصول على جميع السجلات الحرجة"""
        return [log for log in self.logs if log.severity == "CRITICAL"]

    def get_unresolved_logs(self) -> List[WarningEntry]:
        """الحصول على جميع السجلات غير المحلولة"""
        return [log for log in self.logs if not log.resolved]

    def generate_report(self) -> str:
        """
        توليد تقرير شامل عن السجلات

        Returns:
            تقرير نصي مفصل
        """
        stats = self.detector.get_statistics()

        report_lines = [
            "=" * 70,
            "📊 تقرير نظام سجلات التحذير الوراثي",
            "=" * 70,
            "",
            "📈 الإحصائيات العامة:",
            f"   إجمالي الفحوصات: {stats['total_checks']}",
            f"   التشوهات المكتشفة: {stats['anomalies_detected']}",
            f"   الأحداث الحرجة: {stats['critical_events']}",
            f"   مستوى التنبيه الحالي: {stats['alert_level']}",
            f"   المراقبة نشطة: {stats['monitoring_active']}",
            f"   معدل الكشف: {stats['detection_rate']:.4f}",
            "",
            "📊 توزيع الشدة:",
        ]

        for severity, count in stats['severity_breakdown'].items():
            bar = "█" * min(count, 50)
            report_lines.append(f"   {severity:10s} │{bar}│ {count}")

        report_lines.extend([
            "",
            "⚠️ السجلات غير المحلولة:",
        ])

        unresolved = self.get_unresolved_logs()
        if unresolved:
            for log in unresolved[-10:]:  # آخر 10 فقط
                report_lines.append(f"   • [{log.severity}] {log.id}: {log.description[:50]}...")
        else:
            report_lines.append("   ✅ لا توجد سجلات غير محلولة")

        report_lines.extend([
            "",
            "🛑 الأحداث الحرجة:",
        ])

        critical = self.get_critical_logs()
        if critical:
            for log in critical[-5:]:  # آخر 5 فقط
                report_lines.append(f"   • {log.id}: {log.description[:50]}...")
        else:
            report_lines.append("   ✅ لا توجد أحداث حرجة")

        report_lines.extend([
            "",
            "=" * 70,
            f"تاريخ التقرير: {datetime.now().isoformat()}",
            "=" * 70
        ])

        return "\n".join(report_lines)

    def export_all_logs(self, output_file: str = "all_warnings.json") -> str:
        """
        تصدير جميع السجلات إلى ملف JSON

        Args:
            output_file: اسم ملف الإخراج

        Returns:
            مسار الملف المُصدّر
        """
        filepath = os.path.join(self.log_directory, output_file)

        export_data = {
            'export_timestamp': time.time(),
            'total_logs': len(self.logs),
            'statistics': self.detector.get_statistics(),
            'logs': [log.to_dict() for log in self.logs]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"📦 تم تصدير {len(self.logs)} سجل إلى: {filepath}")

        return filepath


# === تجربة توضيحية ===
if __name__ == "__main__":
    print("=" * 70)
    print("⚠️ Platinum African Project - Genetic Warning Log System")
    print("   نظام سجلات تحذير التشوهات الوراثية")
    print("=" * 70)

    # تهيئة النظام
    log_system = WarningLogSystem(log_directory="genetic_encryption/warning_logs")

    print("\n🔍 بدء محاكاة المراقبة...")

    # سيناريو 1: بيانات سليمة
    print("\n" + "-" * 70)
    print("سيناريو 1: بيانات وراثية سليمة")
    healthy_data = np.random.randn(1000) * 0.5 + 10
    result1 = log_system.log_anomaly(healthy_data, "genetic_encoder_v1")
    if result1 is None:
        print("✅ لا توجد تشوهات - البيانات سليمة")

    # سيناريو 2: بيانات بها تشوه طفيف
    print("\n" + "-" * 70)
    print("سيناريو 2: تشوه طفيف في البيانات")
    corrupted_data_low = np.random.randn(1000) * 0.5 + 10
    corrupted_data_low[::10] *= 5  # بعض القيم الشاذة
    result2 = log_system.log_anomaly(corrupted_data_low, "epigenetic_modifier")

    # سيناريو 3: بيانات بها تشوه حرج
    print("\n" + "-" * 70)
    print("سيناريو 3: تشوه حرج في البيانات")
    corrupted_data_critical = np.random.randn(1000) * 2 + 10
    corrupted_data_critical[::3] *= 20  # العديد من القيم الشاذة
    result3 = log_system.log_anomaly(corrupted_data_critical, "quantum_encryptor")

    # سيناريو 4: محاولة اختراق
    print("\n" + "-" * 70)
    print("سيناريو 4: محاولة وصول غير مصرح به")
    intrusion_data = np.random.randn(500) * 5
    result4 = log_system.detector._create_warning_entry(
        anomaly_type=AnomalyType.UNAUTHORIZED_ACCESS,
        severity=SeverityLevel.HIGH,
        affected_module="access_control",
        description="محاولة وصول غير مصرح به للسجل الوراثي",
        recovery_action="عزل القناة | تغيير المفاتيح | إشعار الأمن",
        human_impact_assessment="POTENTIAL - خطر اختراق بيانات",
        data_snapshot={'attempt_count': 3, 'source_ip': '192.168.x.x'}
    )
    log_system.logs.append(result4)

    # عرض الإحصائيات
    print("\n" + "=" * 70)
    print("📊 إحصائيات النظام:")
    stats = log_system.detector.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # عرض التقرير
    print("\n" + "=" * 70)
    report = log_system.generate_report()
    print(report)

    # تصدير السجلات
    print("\n📦 تصدير السجلات...")
    export_path = log_system.export_all_logs()

    print("\n" + "=" * 70)
    print("✨ اكتملت تجربة نظام السجلات بنجاح!")
    print("=" * 70)