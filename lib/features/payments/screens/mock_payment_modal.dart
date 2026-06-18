import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_text_styles.dart';
import '../../../core/utils/currency_formatter.dart';

class MockPaymentModal extends StatefulWidget {
  final double amount;
  final String projectName;
  final VoidCallback onSuccess;

  const MockPaymentModal({
    super.key,
    required this.amount,
    required this.projectName,
    required this.onSuccess,
  });

  static Future<void> show(BuildContext context, {
    required double amount,
    required String projectName,
    required VoidCallback onSuccess,
  }) {
    return showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => MockPaymentModal(
        amount: amount,
        projectName: projectName,
        onSuccess: onSuccess,
      ),
    );
  }

  @override
  State<MockPaymentModal> createState() => _MockPaymentModalState();
}

class _MockPaymentModalState extends State<MockPaymentModal> {
  int _step = 1; // 1: Selection, 2: Form, 3: Success
  int _selectedMethod = 0;
  bool _isProcessing = false;

  final _formKey = GlobalKey<FormState>();
  String? _selectedBank;

  final List<Map<String, dynamic>> _methods = [
    {'icon': Icons.account_balance_wallet_rounded, 'title': 'UPI / QR'},
    {'icon': Icons.credit_card_rounded, 'title': 'Credit / Debit Card'},
    {'icon': Icons.account_balance_rounded, 'title': 'Net Banking'},
  ];

  final List<String> _banks = [
    'HDFC Bank', 'State Bank of India', 'ICICI Bank', 'Axis Bank', 'Kotak Mahindra Bank'
  ];

  void _goToForm() {
    setState(() {
      _step = 2;
    });
  }

  void _processPayment() async {
    if (_formKey.currentState != null && !_formKey.currentState!.validate()) {
      return; // Validation failed
    }

    if (_selectedMethod == 2 && _selectedBank == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Please select a bank')));
      return;
    }

    setState(() {
      _isProcessing = true;
    });

    // Simulate network
    await Future.delayed(const Duration(seconds: 2));

    if (!mounted) return;
    setState(() {
      _isProcessing = false;
      _step = 3;
    });

    // Success animation delay
    await Future.delayed(const Duration(milliseconds: 1500));

    if (!mounted) return;
    Navigator.of(context).pop();
    widget.onSuccess();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final surfaceColor = isDark ? AppColors.surfaceDark : AppColors.surfaceLight;
    final bottomPadding = MediaQuery.of(context).viewInsets.bottom;

    return Container(
      decoration: BoxDecoration(
        color: surfaceColor,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      padding: EdgeInsets.only(
        left: 24,
        right: 24,
        top: 24,
        bottom: bottomPadding > 0 ? bottomPadding + 24 : MediaQuery.of(context).padding.bottom + 24,
      ),
      child: AnimatedSize(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Header
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    if (_step == 2) ...[
                      IconButton(
                        icon: const Icon(Icons.arrow_back_rounded),
                        padding: EdgeInsets.zero,
                        constraints: const BoxConstraints(),
                        onPressed: _isProcessing ? null : () => setState(() => _step = 1),
                      ),
                      const SizedBox(width: 12),
                    ],
                    Text('TaskLance Secure Checkout', style: AppTextStyles.titleMedium),
                  ],
                ),
                IconButton(
                  icon: const Icon(Icons.close_rounded),
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(),
                  onPressed: () => Navigator.of(context).pop(),
                ),
              ],
            ),
            const SizedBox(height: 16),
            
            // Amount Details
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.primary.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.primary.withOpacity(0.3)),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(widget.projectName, style: AppTextStyles.bodyMedium, maxLines: 1, overflow: TextOverflow.ellipsis),
                        const SizedBox(height: 4),
                        Text('Total Payable', style: AppTextStyles.labelSmall),
                      ],
                    ),
                  ),
                  Text(
                    CurrencyFormatter.format(widget.amount),
                    style: AppTextStyles.displayMedium.copyWith(color: AppColors.primary),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            
            if (_step == 3) ...[
              // Success Step
              const SizedBox(height: 32),
              Center(
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.green.withOpacity(0.1),
                  ),
                  child: const Icon(Icons.check_circle_rounded, color: Colors.green, size: 64),
                ),
              ),
              const SizedBox(height: 16),
              Center(child: Text('Payment Successful!', style: AppTextStyles.titleLarge.copyWith(color: Colors.green))),
              const SizedBox(height: 32),
            ] else if (_step == 2) ...[
              // Form Step
              Text('Enter Payment Details', style: AppTextStyles.labelMedium),
              const SizedBox(height: 16),
              Form(
                key: _formKey,
                child: Column(
                  children: [
                    if (_selectedMethod == 0) // UPI
                      TextFormField(
                        decoration: const InputDecoration(
                          labelText: 'UPI ID',
                          hintText: 'e.g., john@okhdfcbank',
                          prefixIcon: Icon(Icons.account_balance_wallet_rounded),
                        ),
                        validator: (val) {
                          if (val == null || val.isEmpty) return 'UPI ID is required';
                          if (!val.contains('@')) return 'Invalid UPI format (must contain @)';
                          if (val.length < 5) return 'UPI ID is too short';
                          return null;
                        },
                      )
                    else if (_selectedMethod == 1) // Card
                      Column(
                        children: [
                          TextFormField(
                            decoration: const InputDecoration(
                              labelText: 'Card Number',
                              hintText: '1234 5678 9101 1121',
                              prefixIcon: Icon(Icons.credit_card_rounded),
                            ),
                            keyboardType: TextInputType.number,
                            inputFormatters: [FilteringTextInputFormatter.digitsOnly, LengthLimitingTextInputFormatter(16)],
                            validator: (val) {
                              if (val == null || val.isEmpty) return 'Card Number is required';
                              if (val.length != 16) return 'Must be exactly 16 digits';
                              return null;
                            },
                          ),
                          const SizedBox(height: 16),
                          Row(
                            children: [
                              Expanded(
                                child: TextFormField(
                                  decoration: const InputDecoration(
                                    labelText: 'Expiry (MM/YY)',
                                    hintText: '12/25',
                                  ),
                                  keyboardType: TextInputType.number,
                                  inputFormatters: [LengthLimitingTextInputFormatter(5)],
                                  validator: (val) {
                                    if (val == null || val.isEmpty) return 'Required';
                                    if (!RegExp(r'^(0[1-9]|1[0-2])\/?([0-9]{2})$').hasMatch(val)) {
                                      return 'Invalid format';
                                    }
                                    return null;
                                  },
                                ),
                              ),
                              const SizedBox(width: 16),
                              Expanded(
                                child: TextFormField(
                                  decoration: const InputDecoration(
                                    labelText: 'CVV',
                                    hintText: '123',
                                  ),
                                  keyboardType: TextInputType.number,
                                  obscureText: true,
                                  inputFormatters: [FilteringTextInputFormatter.digitsOnly, LengthLimitingTextInputFormatter(3)],
                                  validator: (val) {
                                    if (val == null || val.isEmpty) return 'Required';
                                    if (val.length != 3) return '3 digits required';
                                    return null;
                                  },
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          TextFormField(
                            decoration: const InputDecoration(
                              labelText: 'Cardholder Name',
                              hintText: 'John Doe',
                            ),
                            validator: (val) {
                              if (val == null || val.trim().isEmpty) return 'Name is required';
                              return null;
                            },
                          ),
                        ],
                      )
                    else if (_selectedMethod == 2) // Netbanking
                      DropdownButtonFormField<String>(
                        decoration: const InputDecoration(
                          labelText: 'Select Bank',
                          prefixIcon: Icon(Icons.account_balance_rounded),
                        ),
                        items: _banks.map((bank) => DropdownMenuItem(value: bank, child: Text(bank))).toList(),
                        onChanged: (val) => setState(() => _selectedBank = val),
                        validator: (val) {
                          if (val == null || val.isEmpty) return 'Bank selection is required';
                          return null;
                        },
                      ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _isProcessing ? null : _processPayment,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  minimumSize: const Size.fromHeight(56),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: _isProcessing
                    ? const SizedBox(
                        width: 24,
                        height: 24,
                        child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                      )
                    : Text('Pay ${CurrencyFormatter.format(widget.amount)}', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ] else ...[
              // Selection Step
              Text('Select Payment Method', style: AppTextStyles.labelMedium),
              const SizedBox(height: 12),
              ...List.generate(_methods.length, (index) {
                final isSelected = _selectedMethod == index;
                return Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: InkWell(
                    onTap: () {
                      setState(() => _selectedMethod = index);
                    },
                    borderRadius: BorderRadius.circular(12),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: isSelected ? AppColors.primary : (isDark ? AppColors.borderDark : AppColors.borderLight),
                          width: isSelected ? 2 : 1,
                        ),
                        borderRadius: BorderRadius.circular(12),
                        color: isSelected ? AppColors.primary.withOpacity(0.05) : Colors.transparent,
                      ),
                      child: Row(
                        children: [
                          Icon(_methods[index]['icon'] as IconData, 
                            color: isSelected ? AppColors.primary : (isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight),
                          ),
                          const SizedBox(width: 16),
                          Text(_methods[index]['title'] as String, style: AppTextStyles.bodyMedium.copyWith(
                            fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
                          )),
                          const Spacer(),
                          if (isSelected)
                            const Icon(Icons.radio_button_checked_rounded, color: AppColors.primary)
                          else
                            Icon(Icons.radio_button_off_rounded, color: isDark ? AppColors.borderDark : AppColors.borderLight),
                        ],
                      ),
                    ),
                  ),
                );
              }),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _goToForm,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  minimumSize: const Size.fromHeight(56),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('Continue', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
