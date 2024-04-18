# Generated by Django 3.1.5 on 2024-04-18 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialBidDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sNo', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PageOneDetails',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='iwdModuleV2.projects')),
                ('aESFile', models.FileField(null=True, upload_to='')),
                ('dASA', models.DateField(null=True)),
                ('nitNiqNo', models.IntegerField(null=True)),
                ('proTh', models.CharField(max_length=200, null=True)),
                ('emdDetails', models.CharField(max_length=200, null=True)),
                ('preBidDate', models.DateField(max_length=200, null=True)),
                ('technicalBidDate', models.DateField(null=True)),
                ('financialBidDate', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PageThreeDetails',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='iwdModuleV2.projects')),
                ('extensionOfTime', models.FileField(upload_to='')),
                ('actualCostOfBuilding', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PageTwoDetails',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='iwdModuleV2.projects')),
                ('corrigendum', models.FileField(null=True, upload_to='')),
                ('addendum', models.FileField(null=True, upload_to='')),
                ('preBidMeetingDetails', models.FileField(null=True, upload_to='')),
                ('technicalBidMeetingDetails', models.FileField(null=True, upload_to='')),
                ('technicallyQualifiedAgencies', models.CharField(max_length=200, null=True)),
                ('financialBidMeetingDetails', models.FileField(null=True, upload_to='')),
                ('nameOfLowestAgency', models.CharField(max_length=200, null=True)),
                ('letterOfIntent', models.FileField(null=True, upload_to='')),
                ('workOrder', models.FileField(null=True, upload_to='')),
                ('agreementLetter', models.FileField(null=True, upload_to='')),
                ('milestones', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrderForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issueDate', models.DateField()),
                ('nitNiqNo', models.IntegerField()),
                ('agency', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('time', models.IntegerField()),
                ('monthDay', models.IntegerField()),
                ('startDate', models.DateField()),
                ('completionDate', models.DateField()),
                ('deposit', models.IntegerField()),
                ('contractDay', models.IntegerField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TechnicalBidDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sNo', models.CharField(max_length=200)),
                ('requirements', models.CharField(max_length=200)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TechnicalBidContractorDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.technicalbiddetails')),
            ],
        ),
        migrations.CreateModel(
            name='PreBidDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sNo', models.CharField(max_length=200)),
                ('nameOfParticipants', models.CharField(max_length=200)),
                ('issuesRaised', models.CharField(max_length=200)),
                ('responseDecision', models.CharField(max_length=200)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NoOfTechnicalBidTimes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Milestones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sNo', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('timeAllowed', models.IntegerField()),
                ('amountWithheld', models.IntegerField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects')),
            ],
        ),
        migrations.CreateModel(
            name='LetterOfIntentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nitNiqNo', models.IntegerField()),
                ('dateOfOpening', models.DateField()),
                ('agency', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('tenderValue', models.IntegerField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialContractorDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('estimatedCost', models.IntegerField()),
                ('percentageRelCost', models.IntegerField()),
                ('perFigures', models.IntegerField()),
                ('totalCost', models.IntegerField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.financialbiddetails')),
            ],
        ),
        migrations.AddField(
            model_name='financialbiddetails',
            name='key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects', unique=True),
        ),
        migrations.CreateModel(
            name='ExtensionOfTimeDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sNo', models.CharField(max_length=200)),
                ('hindrance', models.CharField(max_length=200)),
                ('periodOfHindrance', models.IntegerField()),
                ('periodOfExtension', models.IntegerField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects')),
            ],
        ),
        migrations.CreateModel(
            name='CorrigendumTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issueDate', models.DateField()),
                ('nitNo', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('lastDate', models.DateField(null=True)),
                ('lastTime', models.TimeField()),
                ('env1BidOpeningDate', models.DateField()),
                ('env1BidOpeningTime', models.TimeField()),
                ('env2BidOpeningDate', models.DateField()),
                ('env2BidOpeningTime', models.TimeField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('agencyName', models.CharField(max_length=200)),
                ('workName', models.CharField(max_length=200)),
                ('fdrSum', models.IntegerField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AESDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sNo', models.CharField(max_length=100)),
                ('descOfItems', models.CharField(max_length=200)),
                ('unit', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('rate', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects')),
            ],
        ),
        migrations.CreateModel(
            name='Addendum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issueDate', models.DateField()),
                ('nitNiqNo', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('openDate', models.DateField()),
                ('openTime', models.TimeField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iwdModuleV2.projects', unique=True)),
            ],
        ),
    ]
