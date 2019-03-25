# Generated by Django 2.1.7 on 2019-03-08 15:49

from django.db import migrations, models
import django.db.models.deletion


def create_target_data(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    CloudTarget = apps.get_model('cloudlaunch', 'CloudDeploymentTarget')
    Zone = apps.get_model('djcloudbridge', 'Zone')

    for zone in Zone.objects.all():
        new_ct = ContentType.objects.get_for_model(CloudTarget)
        CloudTarget.objects.create(target_zone=zone, polymorphic_ctype=new_ct)


def update_deployment_data(apps, schema_editor):
    Deployment = apps.get_model('cloudlaunch', 'ApplicationDeployment')
    CloudTarget = apps.get_model('cloudlaunch', 'CloudDeploymentTarget')

    for deployment in Deployment.objects.all():
        target = CloudTarget.objects.filter(target_zone__region__cloud__id=deployment.target_cloud.slug).first()
        deployment.deployment_target = target
        deployment.save()


def update_appversion_data(apps, schema_editor):
    AppVersion = apps.get_model('cloudlaunch', 'ApplicationVersion')
    CloudTarget = apps.get_model('cloudlaunch', 'CloudDeploymentTarget')

    for appver in AppVersion.objects.all():
        if appver.default_cloud:
            target = CloudTarget.objects.filter(target_zone__region__cloud__id=appver.default_cloud.slug).first()
            appver.default_target = target
            appver.save()


def update_appversiontargetconfig_data(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    CloudConfig = apps.get_model('cloudlaunch', 'ApplicationVersionCloudConfig')
    CloudTarget = apps.get_model('cloudlaunch', 'CloudDeploymentTarget')

    for cloudCfg in CloudConfig.objects.all():
        new_ct = ContentType.objects.get_for_model(CloudConfig)
        cloudCfg.polymorphic_ctype = new_ct
        cloudCfg.target = CloudTarget.objects.filter(target_zone__region__cloud__id=cloudCfg.cloud.slug).first()
        cloudCfg.save()


def update_usage_data(apps, schema_editor):
    Usage = apps.get_model('cloudlaunch', 'Usage')

    for usage in Usage.objects.all():
        usage.app_version_target_config = usage.app_version_cloud_config
        usage.save()


class AlterBaseOperation(migrations.operations.base.Operation):
    reduce_to_sql = False
    reversible = True

    def __init__(self, model_name, bases, prev_bases):
        self.model_name = model_name
        self.bases = bases
        self.prev_bases = prev_bases

    def state_forwards(self, app_label, state):
        state.models[app_label, self.model_name].bases = self.bases
        state.reload_model(app_label, self.model_name)

    def state_backwards(self, app_label, state):
        state.models[app_label, self.model_name].bases = self.prev_bases
        state.reload_model(app_label, self.model_name)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def describe(self):
        return "Update %s bases to %s" % (self.model_name, self.bases)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('djcloudbridge', '0006_decompose_cloud_and_add_zone'),
        ('cloudlaunch', '0007_delete_user_profile'),
    ]

    # run_before = [
    #     ('djcloudbridge', '0007_delete_cloudold'),
    # ]

    operations = [
        migrations.AlterField(
            model_name='cloudimage',
            name='cloud',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='djcloudbridge.Cloud')
        ),
        migrations.CreateModel(
            name='ApplicationVersionTargetConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_launch_config', models.TextField(blank=True, help_text='Target specific initial configuration data to parameterize the launch with.', max_length=16384, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeploymentTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Deployment Target',
                'verbose_name_plural': 'Deployment Targets',
            },
        ),
        migrations.AlterModelOptions(
            name='applicationversioncloudconfig',
            options={'base_manager_name': 'objects'},
        ),
        migrations.CreateModel(
            name='CloudDeploymentTarget',
            fields=[
                ('deploymenttarget_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cloudlaunch.DeploymentTarget')),
                ('target_zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djcloudbridge.Zone')),
            ],
            options={
                'verbose_name': 'Cloud',
                'verbose_name_plural': 'Clouds',
            },
            bases=('cloudlaunch.deploymenttarget',),
        ),
        migrations.CreateModel(
            name='HostDeploymentTarget',
            fields=[
                ('deploymenttarget_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cloudlaunch.DeploymentTarget')),
            ],
            options={
                'verbose_name': 'Host',
                'verbose_name_plural': 'Hosts',
            },
            bases=('cloudlaunch.deploymenttarget',),
        ),
        migrations.CreateModel(
            name='KubernetesDeploymentTarget',
            fields=[
                ('deploymenttarget_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cloudlaunch.DeploymentTarget')),
                ('kube_config', models.CharField(max_length=16384)),
            ],
            options={
                'verbose_name': 'Kubernetes Cluster',
                'verbose_name_plural': 'Kubernetes Clusters',
            },
            bases=('cloudlaunch.deploymenttarget',),
        ),
        migrations.AddField(
            model_name='deploymenttarget',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_cloudlaunch.deploymenttarget_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='applicationversiontargetconfig',
            name='application_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_version_config', to='cloudlaunch.ApplicationVersion'),
        ),
        migrations.AddField(
            model_name='applicationversiontargetconfig',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_cloudlaunch.applicationversiontargetconfig_set+', to='contenttypes.ContentType'),
        ),
        # Temporarily allow nulls
        migrations.AddField(
            model_name='applicationversiontargetconfig',
            name='target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='app_version_config', to='cloudlaunch.DeploymentTarget'),
        ),
        migrations.RemoveField(
            model_name='applicationdeployment',
            name='provider_settings',
        ),
        migrations.RunPython(create_target_data),
        migrations.AddField(
            model_name='applicationdeployment',
            name='deployment_target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='cloudlaunch.DeploymentTarget'),
        ),
        migrations.RunPython(update_deployment_data),
        migrations.AlterField(
            model_name='applicationdeployment',
            name='deployment_target',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE,
                                    to='cloudlaunch.DeploymentTarget')
        ),
        migrations.RemoveField(
            model_name='applicationdeployment',
            name='target_cloud',
        ),
        migrations.AddField(
            model_name='applicationversion',
            name='default_target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='+', to='cloudlaunch.DeploymentTarget'),
        ),
        migrations.RunPython(update_appversion_data),
        migrations.RemoveField(
            model_name='applicationversion',
            name='default_cloud',
        ),
        migrations.AlterField(
            model_name='applicationdeployment',
            name='credentials',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_creds',
                                    to='djcloudbridge.Credentials'),
        ),
        migrations.AlterField(
            model_name='applicationversioncloudconfig',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='cloudlaunch.CloudImage'),
        ),
        migrations.AlterField(
            model_name='usage',
            name='app_deployment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                    to='cloudlaunch.ApplicationDeployment'),
        ),
        migrations.AddField(
            model_name='applicationversioncloudconfig',
            name='applicationversiontargetconfig_ptr',
            field=models.OneToOneField(auto_created=False, null=True,
                                       on_delete=django.db.models.deletion.CASCADE,
                                       parent_link=True, primary_key=False, serialize=False,
                                       to='cloudlaunch.ApplicationVersionTargetConfig'),
            preserve_default=False,
        ),
        migrations.RunSQL(
            sql="UPDATE cloudlaunch_applicationversioncloudconfig SET applicationversiontargetconfig_ptr_id = id; "
                "INSERT INTO cloudlaunch_applicationversiontargetconfig SELECT id, default_launch_config, application_version_id, NULL, NULL"
                " FROM cloudlaunch_applicationversioncloudconfig;",
        ),
        migrations.RemoveField(
            model_name='applicationversioncloudconfig',
            name='id',
        ),
        migrations.AlterField(
            model_name='applicationversioncloudconfig',
            name='applicationversiontargetconfig_ptr',
            field=models.OneToOneField(auto_created=True,
                                       on_delete=django.db.models.deletion.CASCADE,
                                       parent_link=True, primary_key=True, serialize=False,
                                       to='cloudlaunch.ApplicationVersionTargetConfig'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='applicationversioncloudconfig',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='applicationversioncloudconfig',
            name='application_version',
        ),
        migrations.RemoveField(
            model_name='applicationversioncloudconfig',
            name='default_instance_type',
        ),
        migrations.RemoveField(
            model_name='applicationversioncloudconfig',
            name='default_launch_config',
        ),
        AlterBaseOperation(
            model_name='applicationversioncloudconfig',
            bases=('cloudlaunch.applicationversiontargetconfig',),
            prev_bases=tuple()
        ),
        migrations.RunPython(update_appversiontargetconfig_data),
        migrations.RemoveField(
            model_name='applicationversioncloudconfig',
            name='cloud',
        ),
        migrations.AlterUniqueTogether(
            name='applicationversiontargetconfig',
            unique_together={('application_version', 'target')},
        ),
        # Undo make nullable
        migrations.AlterField(
            model_name='applicationversiontargetconfig',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='app_version_config', to='cloudlaunch.DeploymentTarget'),
            preserve_default=False,
        ),
        # Temporarily make nullable
        migrations.AddField(
            model_name='usage',
            name='app_version_target_config',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                    to='cloudlaunch.ApplicationVersionTargetConfig'),
            preserve_default=False,
        ),
        migrations.RunPython(update_usage_data),
        # Undo make nullable
        migrations.AlterField(
            model_name='usage',
            name='app_version_target_config',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                    to='cloudlaunch.ApplicationVersionTargetConfig'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='usage',
            name='app_version_cloud_config',
        ),
        migrations.AlterUniqueTogether(
            name='clouddeploymenttarget',
            unique_together={('deploymenttarget_ptr', 'target_zone')},
        ),
    ]